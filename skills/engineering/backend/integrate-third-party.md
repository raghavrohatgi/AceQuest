# Skill: Integrate Third-Party Service

## Purpose
Provide a standardised pattern for integrating external APIs and SDKs into AceQuest's backend. Covers vendor client initialisation, secret management, error normalisation, retry logic, circuit-breaking, and webhook verification. Examples use Razorpay (payments), Twilio (SMS OTP), and AWS S3 (media uploads) — the same pattern applies to any vendor.

## Used By
- Backend Engineer Agent
- DevOps Agent
- Full-Stack Engineer Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `vendor` | string | Name of the third-party service, e.g. `razorpay`, `twilio`, `aws-s3` |
| `purpose` | string | What AceQuest uses it for, e.g. `subscription payments` |
| `sdkPackage` | string | npm package name |
| `secretEnvVars` | string[] | Environment variable names for credentials |
| `webhookSecret` | string | Env var name for webhook signature verification |
| `retryable` | boolean | Whether transient failures should be retried |

## Procedure / Template

### Step 1 — Install SDK and Add Types

```bash
npm install razorpay axios-retry p-retry
npm install --save-dev @types/razorpay
```

### Step 2 — Centralise Secrets Validation at Boot

```typescript
// src/config/env.ts
import { z } from "zod";

const EnvSchema = z.object({
  // Razorpay
  RAZORPAY_KEY_ID: z.string().min(1),
  RAZORPAY_KEY_SECRET: z.string().min(1),
  RAZORPAY_WEBHOOK_SECRET: z.string().min(1),
  // Twilio
  TWILIO_ACCOUNT_SID: z.string().startsWith("AC"),
  TWILIO_AUTH_TOKEN: z.string().min(1),
  TWILIO_VERIFY_SERVICE_SID: z.string().startsWith("VA"),
  // AWS
  AWS_ACCESS_KEY_ID: z.string().min(16),
  AWS_SECRET_ACCESS_KEY: z.string().min(1),
  AWS_S3_BUCKET: z.string().min(1),
  AWS_REGION: z.string().min(1),
});

export const env = EnvSchema.parse(process.env);
```

### Step 3 — Create a Vendor Client Singleton

```typescript
// src/lib/razorpay.ts
import Razorpay from "razorpay";
import { env } from "../config/env";

export const razorpay = new Razorpay({
  key_id: env.RAZORPAY_KEY_ID,
  key_secret: env.RAZORPAY_KEY_SECRET,
});
```

### Step 4 — Wrap Vendor Calls in a Service

Never call a third-party SDK directly from a controller. Wrap it in a typed service that normalises errors.

```typescript
// src/services/payment.service.ts
import { razorpay } from "../lib/razorpay";
import { AppError } from "../utils/AppError";
import { logger } from "../utils/logger";
import pRetry from "p-retry";

export interface CreateOrderInput {
  studentId: string;
  planId: string;
  amountPaise: number;  // Razorpay uses paise (1 INR = 100 paise)
  currency?: string;
}

export interface CreateOrderOutput {
  orderId: string;
  amount: number;
  currency: string;
  keyId: string;
}

export class PaymentService {
  async createOrder(input: CreateOrderInput): Promise<CreateOrderOutput> {
    logger.info("payment.createOrder.start", {
      studentId: input.studentId,
      planId: input.planId,
      amountPaise: input.amountPaise,
    });

    let order: any;
    try {
      order = await pRetry(
        () =>
          razorpay.orders.create({
            amount: input.amountPaise,
            currency: input.currency ?? "INR",
            receipt: `plan_${input.planId}_${Date.now()}`,
            notes: { studentId: input.studentId, planId: input.planId },
          }),
        {
          retries: 3,
          factor: 2,
          minTimeout: 500,
          onFailedAttempt: (err) => {
            logger.warn("payment.createOrder.retry", {
              attempt: err.attemptNumber,
              retriesLeft: err.retriesLeft,
              error: err.message,
            });
          },
        }
      );
    } catch (err: any) {
      logger.error("payment.createOrder.failed", { error: err.message, studentId: input.studentId });
      throw new AppError("Payment gateway unavailable. Please try again.", 502, "PAYMENT_GATEWAY_ERROR");
    }

    logger.info("payment.createOrder.success", { orderId: order.id });
    return {
      orderId: order.id,
      amount: order.amount,
      currency: order.currency,
      keyId: process.env.RAZORPAY_KEY_ID!,
    };
  }
}
```

### Step 5 — Webhook Verification Middleware

```typescript
// src/middleware/verifyWebhook.ts
import { Request, Response, NextFunction } from "express";
import crypto from "crypto";
import { env } from "../config/env";
import { AppError } from "../utils/AppError";

export function verifyRazorpayWebhook(
  req: Request,
  _res: Response,
  next: NextFunction
): void {
  const signature = req.headers["x-razorpay-signature"] as string;
  if (!signature) return next(new AppError("Missing webhook signature", 400, "MISSING_SIGNATURE"));

  // req.rawBody must be populated — use express.raw() for this route only
  const hmac = crypto
    .createHmac("sha256", env.RAZORPAY_WEBHOOK_SECRET)
    .update(req.rawBody ?? "")
    .digest("hex");

  if (!crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(signature))) {
    return next(new AppError("Webhook signature mismatch", 401, "INVALID_SIGNATURE"));
  }
  next();
}
```

Mount the webhook route **before** `express.json()` so the raw body is preserved:

```typescript
// src/app.ts  (excerpt)
app.post(
  "/webhooks/razorpay",
  express.raw({ type: "application/json" }),
  verifyRazorpayWebhook,
  paymentController.handleWebhook
);
```

### Step 6 — Presigned S3 Upload URLs

```typescript
// src/services/media.service.ts
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { v4 as uuidv4 } from "uuid";
import { env } from "../config/env";

const s3 = new S3Client({ region: env.AWS_REGION });

const ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/webp", "video/mp4"];
const MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10 MB

export class MediaService {
  async getUploadUrl(
    studentId: string,
    mimeType: string,
    sizeBytes: number
  ): Promise<{ uploadUrl: string; fileKey: string }> {
    if (!ALLOWED_MIME_TYPES.includes(mimeType)) {
      throw new AppError(`Unsupported file type: ${mimeType}`, 422, "INVALID_MIME_TYPE");
    }
    if (sizeBytes > MAX_SIZE_BYTES) {
      throw new AppError("File exceeds 10 MB limit", 422, "FILE_TOO_LARGE");
    }

    const fileKey = `uploads/${studentId}/${uuidv4()}`;
    const command = new PutObjectCommand({
      Bucket: env.AWS_S3_BUCKET,
      Key: fileKey,
      ContentType: mimeType,
      ContentLength: sizeBytes,
      Metadata: { studentId },
    });

    const uploadUrl = await getSignedUrl(s3, command, { expiresIn: 300 }); // 5 min
    return { uploadUrl, fileKey };
  }
}
```

### Step 7 — Twilio OTP (SMS Verification)

```typescript
// src/services/otp.service.ts
import twilio from "twilio";
import { env } from "../config/env";
import { AppError } from "../utils/AppError";

const client = twilio(env.TWILIO_ACCOUNT_SID, env.TWILIO_AUTH_TOKEN);

export class OTPService {
  async sendOTP(phoneNumber: string): Promise<void> {
    try {
      await client.verify.v2
        .services(env.TWILIO_VERIFY_SERVICE_SID)
        .verifications.create({ to: phoneNumber, channel: "sms" });
    } catch (err: any) {
      throw new AppError("Failed to send OTP", 502, "OTP_SEND_FAILED");
    }
  }

  async verifyOTP(phoneNumber: string, code: string): Promise<boolean> {
    try {
      const check = await client.verify.v2
        .services(env.TWILIO_VERIFY_SERVICE_SID)
        .verificationChecks.create({ to: phoneNumber, code });
      return check.status === "approved";
    } catch {
      return false;
    }
  }
}
```

## Output
- `src/config/env.ts` — Zod-validated environment schema
- `src/lib/<vendor>.ts` — initialised SDK singleton
- `src/services/<domain>.service.ts` — wrapped, error-normalised service
- `src/middleware/verifyWebhook.ts` — HMAC signature verification
- `.env.example` updated with all new variable names

## Quality Checks
- [ ] All credentials come from `process.env`; none are hardcoded or committed
- [ ] `.env.example` lists every new variable with a placeholder value
- [ ] Vendor SDK is instantiated once (singleton), not per-request
- [ ] `p-retry` or equivalent wraps network calls with exponential back-off (max 3 retries)
- [ ] Vendor errors are caught and re-thrown as `AppError` with `5xx` status codes
- [ ] Webhooks use `timingSafeEqual` for HMAC comparison (prevents timing attacks)
- [ ] Raw body is preserved for webhook routes using `express.raw()`
- [ ] File upload routes validate MIME type and size before issuing presigned URLs
- [ ] Integration tests mock the SDK at the module boundary (no real API calls in CI)

## Example

```
POST /api/v1/payments/create-order
Authorization: Bearer <student-jwt>
Content-Type: application/json

{ "planId": "plan_annual_2025", "amountPaise": 99900 }

→ 201 Created
{
  "success": true,
  "data": {
    "orderId": "order_MxyzABCDEFGH",
    "amount": 99900,
    "currency": "INR",
    "keyId": "rzp_live_XXXXXXXXXXXX"
  }
}
```
