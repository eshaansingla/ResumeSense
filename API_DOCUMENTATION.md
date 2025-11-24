# ResumeSense API Documentation

Complete API reference for ResumeSense backend endpoints.

## Base URL

```
http://localhost:5000/api
```

## Endpoints

### 1. Analyze Resume

**Endpoint:** `POST /api/analyze`

Analyzes a resume and optionally matches it against a job description.

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `resume_file` (file, optional): PDF file of the resume
  - `resume_text` (string, optional): Plain text resume content
  - `job_description` (string, optional): Job description text

**Note:** Either `resume_file` or `resume_text` must be provided.

**Response (200 OK):**
```json
{
  "match_score": 85.5,
  "ats_score": 92.3,
  "quality_score": 88.7,
  "match_details": {
    "common_keywords": ["Python", "JavaScript", "Flask"],
    "missing_keywords": ["Docker", "Kubernetes"],
    "important_keywords_matched": 8,
    "important_keywords_total": 10,
    "matched_important_keywords": ["Python", "JavaScript"]
  },
  "ats_report": {
    "issues": ["Missing phone number"],
    "recommendations": [
      "Include a phone number",
      "Use bullet points to improve readability"
    ],
    "section_checks": {
      "education": true,
      "experience": true,
      "skills": true,
      "contact": true,
      "summary": true
    },
    "contact_check": {
      "has_email": true,
      "has_phone": false,
      "has_address": true,
      "complete": false
    },
    "formatting_checks": {
      "has_tables": false,
      "excessive_formatting": false,
      "has_headers_footers": false,
      "has_bullets": true
    }
  },
  "power_verbs": {
    "findings": [
      {
        "weak_verb": "did",
        "suggestions": ["executed", "implemented", "accomplished"],
        "context": "I did some work on the project...",
        "position": 123
      }
    ],
    "stats": {
      "weak_verb_count": 3,
      "strong_verb_count": 15,
      "weak_verbs_found": [
        {"verb": "did", "count": 2},
        {"verb": "made", "count": 1}
      ],
      "power_verb_score": 83.3
    }
  },
  "quality_details": {
    "model_used": "ml_model",
    "features": {
      "text_length": 2500,
      "word_count": 450,
      "keyword_density": 0.75,
      "action_verbs_count": 15,
      "ats_score": 0.923,
      ...
    }
  },
  "analysis_id": 1,
  "resume_id": 1,
  "job_id": 1
}
```

**Error Responses:**

- `400 Bad Request`: Missing resume or invalid file
```json
{
  "error": "No resume provided. Please upload a PDF file or provide resume text."
}
```

- `500 Internal Server Error`: Server error during analysis
```json
{
  "error": "An error occurred during analysis: [error message]"
}
```

---

### 2. Get Analysis History

**Endpoint:** `GET /api/history`

Retrieves past analysis results.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of results to return (default: 20, max: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "resume_id": 1,
    "job_id": 1,
    "match_score": 85.5,
    "ats_score": 92.3,
    "quality_score": 88.7,
    "created_at": "2024-01-15T10:30:00",
    "resume_preview": "John Doe\nSoftware Engineer\nEmail: john@email.com...",
    "jd_preview": "Software Engineer - Full Stack Developer\nCompany: Tech Corp..."
  },
  {
    "id": 2,
    "resume_id": 2,
    "job_id": null,
    "match_score": null,
    "ats_score": 78.5,
    "quality_score": 75.2,
    "created_at": "2024-01-14T15:20:00",
    "resume_preview": "...",
    "jd_preview": null
  }
]
```

**Error Responses:**

- `500 Internal Server Error`: Database error
```json
{
  "error": "An error occurred retrieving history: [error message]"
}
```

---

### 3. Get Resume by ID

**Endpoint:** `GET /api/resume/<id>`

Retrieves a specific resume by its ID.

**URL Parameters:**
- `id` (integer, required): Resume ID

**Response (200 OK):**
```json
{
  "id": 1,
  "resume_text": "John Doe\nSoftware Engineer\n...",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**

- `404 Not Found`: Resume not found
```json
{
  "error": "Resume not found"
}
```

- `500 Internal Server Error`: Server error
```json
{
  "error": "An error occurred retrieving resume: [error message]"
}
```

---

### 4. Get Analysis Result by ID

**Endpoint:** `GET /api/analysis/<id>`

Retrieves a specific analysis result by its ID.

**URL Parameters:**
- `id` (integer, required): Analysis result ID

**Response (200 OK):**
```json
{
  "id": 1,
  "resume_id": 1,
  "job_id": 1,
  "match_score": 85.5,
  "ats_score": 92.3,
  "quality_score": 88.7,
  "ats_flags": {
    "issues": [],
    "recommendations": [...],
    "section_checks": {...},
    "contact_check": {...},
    "formatting_checks": {...}
  },
  "power_verb_suggestions": {
    "findings": [...],
    "stats": {...}
  },
  "match_details": {
    "common_keywords": [...],
    "missing_keywords": [...],
    ...
  },
  "created_at": "2024-01-15T10:30:00",
  "resume_text": "...",
  "job_description": "..."
}
```

**Error Responses:**

- `404 Not Found`: Analysis result not found
```json
{
  "error": "Analysis result not found"
}
```

- `500 Internal Server Error`: Server error
```json
{
  "error": "An error occurred retrieving analysis: [error message]"
}
```

---

## Data Models

### Resume
```json
{
  "id": 1,
  "resume_text": "string",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

### Job
```json
{
  "id": 1,
  "job_description": "string",
  "created_at": "ISO 8601 datetime"
}
```

### Analysis Result
```json
{
  "id": 1,
  "resume_id": 1,
  "job_id": 1,
  "match_score": 85.5,
  "ats_score": 92.3,
  "quality_score": 88.7,
  "ats_flags": {},
  "power_verb_suggestions": [],
  "match_details": {},
  "created_at": "ISO 8601 datetime"
}
```

## Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing rate limiting.

## Authentication

Currently, the API does not require authentication. For production, implement:
- API key authentication
- User authentication (JWT tokens)
- Role-based access control

## CORS

CORS is enabled for all origins. For production, restrict to specific domains.

---

**Last Updated:** January 2024


