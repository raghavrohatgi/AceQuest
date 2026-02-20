# Flowchart Guidelines
---
# 📐 System Protocol: Standardized User Flows
## 1. Core Philosophy
To maintain technical accuracy and visual clarity in Excalidraw, all flowcharts must adhere to the **"Atomic & Linear"** principle.
- **Atomic:** Each flowchart describes **one** discrete user goal (e.g., "Login", "Purchase Subscription", "Reset Password"). Do not mix contexts.
- **Linear:** The "Happy Path" (Success Scenario) flows strictly from **Top to Bottom**.
- **Exception Handling:** All Error/Edge cases branch to the **Right** and attempt to return to the main flow.
- **No Overlapping Lines:** Arrows must never cross or overlap other nodes or arrows. Use waypoints or reroute paths to avoid collisions.
- **Decision Branching:** On any `{Decision?}` node — **No always exits Left**, **Yes always continues Right or Down** (happy path).
## 2. The Visual Syntax (Shape Semantics)
We use strict Mermaid.js syntax mapped to standard flowchart symbols.

| **Semantic Role** | **Shape** | **Mermaid Syntax** | **Excalidraw Fill** | **Visual Meaning** |
| --- | --- | --- | --- | --- |
| **Terminator** | **Ellipse (Oval)** | `id([Start / End])` | `#ffc9c9` (pink/red) | Entry or Exit point. Always a verb or noun phrase. |
| **Process** | Rectangle | `id[Action]` | `#EEF2FF` fill, `#4F46E5` border (indigo) | System logic, calculation, or internal state change. |
| **Decision** | **Diamond (Rhombus)** | `id{Question?}` | Default (white fill, dark border) | A binary check. **No → Left branch**, **Yes → Right (down) branch**. Must have labels on all edges. |
| **I/O** | Rectangle | `id[/User Input/]` | `#E0E7FF` fill, `#4F46E5` border (blue) | User interaction (typing, clicking, uploading). |
| **Database** | Rectangle | `id[(Save Data)]` | `#D1FAE5` fill, `#10B981` border (green) | Read/Write operations (DB, LocalStorage, API calls). |
| **Edge Case** | Rectangle | `id[Edge Action]` | `#FEF3C7` fill, `#D97706` border (orange) | Error/alternate path. Always branches **right**. |
| **Connector** | Circle | `id((Ref))` | Default | Jumping to/from a completely different flow (e.g., "Go to Register"). |
| **Notes Box** | Rectangle | *(Excalidraw only — not in Mermaid)* | `#fffbe6` fill, `#faad14` border (yellow) | Developer notes, implementation hints, business rules, API references. Placed beside relevant node. |

### Notes Box Style (Developer Annotations)
- **Shape:** Rectangle (rounded, `roundness: { "type": 3 }`)
- **Fill:** `#fffbe6` (light yellow)
- **Border:** `#faad14` (amber/yellow), dashed stroke
- **Text:** Starts with `📝 Note:` prefix
- **Placement:** Beside (left or right of) the node it annotates, connected with a dashed line if needed
- **Purpose:** Business rules, API endpoint hints, validation logic, edge case explanations, or any info the engineer needs that isn't visible from the flow shape alone
- **NOT part of Mermaid** — add manually in Excalidraw after import

### Terminator Style (Start / End)
- **Shape:** Ellipse (oval), created manually in Excalidraw after Mermaid import
- **Fill:** `#ffc9c9` (pink-red)
- **Border:** `#1e1e1e` (default dark)
- **Text:** Centered inside ellipse
- **Note:** Mermaid `([Text])` imports as a rounded rectangle — manually replace with ellipse shape in Excalidraw after import.
## 3. The "Golden Prompt" for Claude Code
*Copy and paste this instruction block into your session to force the AI to adopt this persona.*
Plaintext
```javascript
*** SYSTEM INSTRUCTION: FLOWCHART GENERATION ***

You are an expert Technical Product Manager. Your goal is to map user flows into Mermaid.js syntax that renders perfectly in Excalidraw.

RULES:
1. DIRECTION: Use `graph TD` (Top-Down).
2. ISOLATION: Map ONLY the requested flow. Use "Connectors" (Circle) for external dependencies.
3. HAPPY PATH: The ideal user journey goes straight down.
4. EDGE CASES: All 'No/Error' branches go to the Right.
5. LABELS: All decision lines MUST have text labels (e.g., `|Yes|`, `|No|`).
6. SYNTAX:
   - Start/End: ([Text])  → import as rounded rect, then manually change to Ellipse in Excalidraw, fill #ffc9c9
   - Process: [Text]      → indigo fill #EEF2FF, border #4F46E5
   - Decision: {Text?}    → Diamond shape, default style. No → Left, Yes → continues down/right
   - Input: [/Text/]      → blue fill #E0E7FF, border #4F46E5
   - Database: [(Text)]   → green fill #D1FAE5, border #10B981
   - Edge Case: [Text]    → orange fill #FEF3C7, border #D97706, branch RIGHT
   - Connector: ((Text))  → default style
   - Notes Box: (Excalidraw only) → yellow fill #fffbe6, amber dashed border #faad14, text starts with "📝 Note:", placed beside relevant node

OUTPUT FORMAT:
Provide ONLY the raw Mermaid code block.
```
## 4. Logical Patterns (How to structure the flow)
### Pattern A: The Decision Gate
*Never leave a decision hanging. Always resolve the negative case.*
- **No → branches Left** (error/retry path)
- **Yes → continues Down** (happy path)
- Lines must NOT cross or overlap any other node/arrow.
Code snippet
```javascript
graph TD
    A[Step 1] --> B{Is Valid?}
    B -- Yes --> C[Proceed]
    B -- No --> D[Show Error]
    D -.-> A
```
### Pattern B: The External Reference
*Do not draw the "Forgot Password" flow inside the "Login" flow. Reference it.*
Code snippet
```javascript
graph TD
    A[/Click Login/] --> B{Forgot Pass?}
    B -- Yes --> C((Go to: Reset Flow))
    B -- No --> D[Validate Creds]
```
## 5. Master Example: "Course Enrollment" Flow
*Use this structure as the template for all future flows.*
Code snippet
```javascript
graph TD
    %% --- NODES ---
    Start([Start: User Clicks 'Buy Course'])
    CheckAuth{Is Logged In?}
    LoginRef((Go to: Login))
    
    ShowPayment[/Display Payment Gateway/]
    InputPayment[/User Enters UPI/Card Details/]
    ProcessPayment[System: Contact Payment Gateway]
    
    PaymentSuccess{Success?}
    ShowError[Display 'Payment Failed']
    
    GrantAccess[(DB: Update User Enrollment)]
    SendEmail[System: Send Welcome Email]
    End([End: Redirect to Course Player])

    %% --- EDGES ---
    Start --> CheckAuth
    
    %% Auth Check
    CheckAuth -- No --> LoginRef
    CheckAuth -- Yes --> ShowPayment
    
    ShowPayment --> InputPayment
    InputPayment --> ProcessPayment
    ProcessPayment --> PaymentSuccess
    
    %% Decision Branching
    PaymentSuccess -- No --> ShowError
    ShowError -.-> InputPayment
    
    %% Happy Path
    PaymentSuccess -- Yes --> GrantAccess
    GrantAccess --> SendEmail
    SendEmail --> End
```
## 6. Import Instructions
1. Copy the code block above.
2. In Excalidraw, select **Tools** > **Mermaid to Excalidraw**.
3. Paste the code.
4. *Note: Excalidraw will automatically convert ****\*\*\*\*\*\*\*\*****\*\*\*\*\*****\*\*\*\*\*****\*\*****`((Circle))`******\*\*\*\*\* to a connector node and \*\*\*\*\*****\*\*\*\*\*\*\*\*\*\*\*\*\***`[(Cylinder)]`**\*\*\*\*\*\*\*\*\*\*\*\*\* to a database node if supported, or standard rectangles if not.*

## 7. Excalidraw JSON Element Format (Required for Text Visibility)

When writing `.excalidraw` files directly as JSON (not via Mermaid import), every element **must** include the following required fields or text will be invisible / nodes will render as empty boxes.

### Required Fields on ALL Elements

Every element (shape, text, arrow) must have:
```json
{
  "angle": 0,
  "strokeStyle": "solid",
  "frameId": null,
  "seed": <unique integer>,
  "version": 1,
  "versionNonce": <unique integer>,
  "isDeleted": false,
  "updated": 1000000000000,
  "link": null,
  "locked": false
}
```

### Text Elements — Additional Required Fields

Text elements (type `"text"`) **must** also include:
```json
{
  "originalText": "<same as text field>",
  "lineHeight": 1.25,
  "containerId": "<id of parent shape, or null if standalone>",
  "baseline": <integer ≈ fontSize × 0.9>
}
```

> ⚠️ **`lineHeight`**** must always be \****`1.25`** — never `1.6666...` or any other value. Using the wrong lineHeight causes text to misalign inside shapes.

### Shape ↔ Text Binding Pattern

**Shapes do NOT carry their label text directly.** Instead:
1. The **shape** element lists the text element in `boundElements`:
```json
{
  "id": "my-shape",
  "type": "rectangle",
  ...
  "boundElements": [{ "type": "text", "id": "my-shape-lbl" }]
}
```
2. The **text** element uses `containerId` to reference its parent shape:
```json
{
  "id": "my-shape-lbl",
  "type": "text",
  "containerId": "my-shape",
  "text": "Label text",
  "originalText": "Label text",
  "lineHeight": 1.25,
  ...
}
```

### Minimal Shape Example (Correct)
```json
{
  "id": "my-rect",
  "type": "rectangle",
  "x": 300, "y": 100, "width": 200, "height": 60,
  "angle": 0,
  "strokeColor": "#4F46E5",
  "backgroundColor": "#EEF2FF",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 1001, "version": 1, "versionNonce": 1001,
  "isDeleted": false,
  "boundElements": [{ "type": "text", "id": "my-rect-lbl" }],
  "updated": 1000000000000,
  "link": null,
  "locked": false
},
{
  "id": "my-rect-lbl",
  "type": "text",
  "x": 310, "y": 118, "width": 180, "height": 25,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 1002, "version": 1, "versionNonce": 1002,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1000000000000,
  "link": null,
  "locked": false,
  "text": "My Label",
  "fontSize": 14,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "baseline": 13,
  "containerId": "my-rect",
  "originalText": "My Label",
  "lineHeight": 1.25
}
```

> ⚠️ **Common Mistake:** Placing `text`, `fontSize`, `fontFamily` etc. directly on the shape element (instead of a separate text child) will result in boxes with no visible text.

### Seed & VersionNonce Uniqueness

Every element must have a **unique** `seed` and `versionNonce` across the entire file. Duplicate values can cause rendering conflicts.

- Use sequential integers starting from a base (e.g., shapes: `1000, 1001, 1002...`, arrows: `3001, 3002...`, text labels: use next available integer).
- Shape and its paired text label must have **different** seed/versionNonce values.
- `updated` should always be `1000000000000` (a fixed large timestamp — do not use `1` or `0`).

## 8. Technical Stack & Syntax
To ensure compatibility between Claude Code and Excalidraw, strict adherence to the **Mermaid.js** library is required.

### Supported Library: `Mermaid.js`
- **Diagram Type:** `graph TD` (Flowchart Top-Down) or `sequenceDiagram`.
- **Rendering:** Native support in GitHub Markdown and Excalidraw.

### Syntax Rules for AI Generation
When generating code, the AI must use these specific Mermaid syntax patterns:
1.  **Nodes:** `id[Text]` (Square) vs `id([Text])` (Rounded).
2.  **Edges:** `-->` (Solid) and `-.->` (Dotted).
3.  **Labels:** `|Yes|` or `|No|` placed directly on edges.
4.  **Styling:** Do NOT add custom CSS/Classes (Excalidraw ignores them). Keep it raw.