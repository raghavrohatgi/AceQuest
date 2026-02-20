# AceQuest API Design Guidelines

## API Structure

### Base URL
```
Production: https://api.acequest.com/v1
Development: http://localhost:3000/api/v1
```

### Resource Naming
- Use **plural nouns** for collections: `/students`, `/assessments`
- Use **kebab-case** for multi-word resources: `/assessment-attempts`
- Nest resources logically: `/students/{id}/progress`

---

## HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve resource(s) | `GET /assessments` |
| POST | Create new resource | `POST /assessments` |
| PATCH | Partially update resource | `PATCH /assessments/{id}` |
| PUT | Replace entire resource | `PUT /assessments/{id}` (rarely used) |
| DELETE | Remove resource | `DELETE /assessments/{id}` |

---

## Status Codes

### Success (2xx)
- **200 OK** - GET, PATCH requests
- **201 Created** - POST requests (include `Location` header)
- **204 No Content** - DELETE requests

### Client Errors (4xx)
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Missing/invalid authentication
- **403 Forbidden** - Authenticated but no permission
- **404 Not Found** - Resource doesn't exist
- **409 Conflict** - Resource conflict (duplicate)
- **422 Unprocessable Entity** - Validation errors
- **429 Too Many Requests** - Rate limit exceeded

### Server Errors (5xx)
- **500 Internal Server Error** - Unexpected error
- **503 Service Unavailable** - Temporary outage

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    "id": "assessment_123",
    "title": "Grade 5 Math",
    "questionCount": 20
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid grade level",
    "details": [
      {
        "field": "gradeLevel",
        "message": "Must be between 3 and 8"
      }
    ]
  }
}
```

### Paginated Response
```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 156,
    "totalPages": 8
  }
}
```

---

## Endpoints

### Authentication
```
POST   /auth/register           # Register new user
POST   /auth/login              # Login
POST   /auth/logout             # Logout
POST   /auth/refresh-token      # Refresh JWT
POST   /auth/forgot-password    # Request password reset
POST   /auth/reset-password     # Reset password
```

### Students
```
GET    /students                # List students (parent/teacher)
GET    /students/{id}           # Get student details
PATCH  /students/{id}           # Update student
DELETE /students/{id}           # Delete student (soft delete)

GET    /students/{id}/progress  # Get progress
GET    /students/{id}/achievements # Get achievements
GET    /students/{id}/badges    # Get earned badges
```

### Assessments
```
GET    /assessments             # List assessments
POST   /assessments             # Create assessment (teacher only)
GET    /assessments/{id}        # Get assessment
PATCH  /assessments/{id}        # Update assessment
DELETE /assessments/{id}        # Delete assessment
POST   /assessments/{id}/publish # Publish assessment

GET    /assessments/{id}/questions # Get questions
POST   /assessments/{id}/start  # Start attempt
POST   /assessments/{id}/submit # Submit answers
```

### Questions
```
GET    /questions               # List questions
POST   /questions               # Create question
GET    /questions/{id}          # Get question
PATCH  /questions/{id}          # Update question
DELETE /questions/{id}          # Delete question
```

### Progress & Analytics
```
GET    /students/{id}/progress             # Overall progress
GET    /students/{id}/progress/{subject}   # Subject-specific
GET    /students/{id}/recommendations      # Next steps
GET    /analytics/dashboard                # Teacher dashboard
```

---

## Query Parameters

### Filtering
```
GET /assessments?gradeLevel=5&subject=math&published=true
```

### Sorting
```
GET /assessments?sortBy=createdAt&order=desc
```

### Pagination
```
GET /assessments?page=2&pageSize=20
```

### Field Selection (Sparse Fieldsets)
```
GET /assessments?fields=id,title,questionCount
```

### Search
```
GET /assessments?search=multiplication
```

---

## Request Body Examples

### Create Assessment
```json
POST /assessments
{
  "title": "Grade 5 Math - Fractions",
  "description": "Assessment covering basic fractions",
  "gradeLevel": 5,
  "subjectId": "math_fractions",
  "timeLimit": 1800,
  "questions": [
    {
      "text": "What is 1/2 + 1/4?",
      "type": "multiple_choice",
      "options": ["3/4", "2/6", "1/6", "3/6"],
      "correctAnswer": 0,
      "difficulty": "medium",
      "points": 10
    }
  ]
}
```

### Submit Assessment
```json
POST /assessments/{id}/submit
{
  "attemptId": "attempt_123",
  "answers": [
    {
      "questionId": "q1",
      "answer": 0,
      "timeSpent": 45
    },
    {
      "questionId": "q2",
      "answer": 2,
      "timeSpent": 62
    }
  ],
  "totalTime": 867
}
```

---

## Headers

### Request Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
Accept: application/json
X-API-Version: 1.0
```

### Response Headers
```
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| Most endpoints | 100 req | 15 min |
| Auth endpoints | 5 req | 15 min |
| Heavy queries | 20 req | 15 min |

---

## Versioning Strategy

- **URL versioning**: `/api/v1/`, `/api/v2/`
- New version for breaking changes
- Support 2 versions simultaneously
- Deprecate old version after 6 months

---

## Security

### Authentication
- JWT tokens (1 hour expiry)
- Refresh tokens (30 days)
- HTTPS only in production

### Input Validation
- Validate all inputs with Zod
- Sanitize HTML/SQL
- Limit request body size (10MB max)

### CORS
- Whitelist allowed origins
- Credentials allowed for app domains

---

## Error Codes

| Code | Meaning |
|------|---------|
| AUTH_REQUIRED | No authentication provided |
| INVALID_TOKEN | Token expired or invalid |
| FORBIDDEN | No permission for action |
| NOT_FOUND | Resource doesn't exist |
| VALIDATION_ERROR | Input validation failed |
| DUPLICATE_ENTRY | Resource already exists |
| RATE_LIMIT_EXCEEDED | Too many requests |
| INTERNAL_ERROR | Server error occurred |

---

## Best Practices

1. ✅ Always return consistent response format
2. ✅ Use proper HTTP status codes
3. ✅ Include error details for debugging
4. ✅ Implement pagination for lists
5. ✅ Cache frequently accessed data
6. ✅ Log all errors with context
7. ✅ Version your API
8. ✅ Document all endpoints
9. ✅ Rate limit all endpoints
10. ✅ Test error scenarios

---

**Remember: Good API design = Happy developers + Reliable systems**
