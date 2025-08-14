# AI-Powered Survey Generator - Backend Implementation

## Overview

This project implements an AI-powered survey generator backend that transforms user descriptions into structured surveys. The system integrates with a React frontend to provide a seamless survey creation experience. The backend uses FastAPI, PostgreSQL, Redis, and Groq API for AI-powered survey generation, and a React frontend for a smooth, responsive UI.

Key features:
- 🧠 AI-powered survey generation using LLMs
- ⚡️ Multi-layer caching (Redis + PostgreSQL)
- 🔒 JWT authentication and rate limiting
- 🚀 Async request processing
- 📊 Structured survey output with multiple question types
- 🔄 Seamless frontend integration

## Tech Stack

###  Backend Core Components
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 16
- **Caching**: Redis
- **AI Integration**: Groq API (LLaMA3-70b model)
- **Authentication**: JWT
- **Rate Limiting**: SlowAPI
- **Logging**: Loguru
- **Retries**: Tenacity

### Key Libraries
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- Redis-py (Redis client)
- Tenacity (Retry logic)
- Loguru (Logging)
- SlowAPI (Rate limiting)
- Groq (LLM integration)

###  Frontend Core Components
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **State Management**: Zustand + Context Provider
- **HTTP Client**: Axios

## Backend Features

### Survey Generation
- Transforms natural language descriptions into structured surveys
- Supports multiple question types:
  - Multiple choice
  - Single choice
  - Open text
  - Short answer
  - Rating scales
  - NPS scores
- Outputs JSON for seamless frontend rendering

### Caching System
- **Redis cache**: First-level cache with TTL (120 seconds)
- **Database cache**: Persistent storage of generated surveys
- **Prompt hashing**: SHA-256 hashing for efficient deduplication

### Security
- JWT authentication with secret key
- Rate limiting (10 requests/minute)
- Request timeouts (30 seconds)
- Input validation and sanitization
- CORS protection

### Reliability
- Retry policies for external services
- Comprehensive error handling
- Health check endpoints
- Request ID tracing
- Async database operations

### Performance
- Async request processing
- Connection pooling
- Minimal cold-start overhead
- Efficient prompt handling

### Frontend Features

### Survey Creation & AI Integration**
- Generate Survey button triggers AI survey creation.
- User can enter only the title or title + description (description is optional).
- Dropdown mode selector beside Generate button (aligned in one row).
- Backend integration with Axios client, token auto-injection.

### Interactive Survey Answering**
- Respond mode allows selecting answers for all question types.
- Scale questions show numeric labels (1–10).
- Cannot submit unless all questions are answered.
- Edit mode retains all options visible for multiple/single-choice questions.
- Edit button expands into duplicate/delete actions.

### Sidebar Navigation**
- Left sidebar lists survey title + questions as an outline.
- Click “Create New Survey” to reset state and start fresh.
- Click question outline items to scroll to that question.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Groq API key (free tier available)
- PostgreSQL 16
- Redis

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mirpasad/boundary-survey.git
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your credentials:
```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET=your_jwt_secret
```

### Running with Docker Compose

1. Start all services:
```bash
docker-compose up --build
```

2. Access services:
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

### Manual Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | *Required* |
| `GROQ_MODEL` | Groq model to use | `llama3-70b-8192` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://survey:survey@db/surveys` |
| `REDIS_HOST` | Redis host | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_CACHE_TTL` | Redis cache TTL in seconds | `120` |
| `JWT_SECRET` | Secret key for JWT tokens | *Required* |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_TTL_SECONDS` | JWT token expiration | `3600` |
| `DEV_LOGIN_EMAIL` | Developer email for testing | `dev@test.com` |
| `DEV_LOGIN_PASSWORD` | Developer password for testing | `devpass` |
| `RATE_LIMIT` | Rate limit configuration | `10/minute` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,*` |
| `GLOBAL_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

## API Documentation

### Authentication
- **POST /api/auth/token**  
  Obtain JWT token for authentication  
  Request body:
  ```json
  {
    "email": "dev@test.com",
    "password": "devpass"
  }
  ```

### Survey Generation
- **POST /api/surveys/generate**  
  Generate survey from description  
  Request body:
  ```json
  {
    "description": "Customer satisfaction for an online store"
  }
  ```
  
  Successful response:
  ```json
  {
    "title": "E-commerce Customer Satisfaction Survey",
    "questions": [
      {
        "type": "multiple_choice",
        "question": "How satisfied are you with our website?",
        "options": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"]
      },
      {
        "type": "rating_scale",
        "question": "Rate your shopping experience",
        "min": 1,
        "max": 5,
        "min_label": "Poor",
        "max_label": "Excellent"
      }
    ]
  }
  ```

### Health Check
- **GET /api/health**  
  Service health check  
  Response: `{"status": "ok"}`

## Project Structure

```
backend/
│
├── router/
│   ├── auth.py
│   └── surveys.py
│   └── __init__.py
│
├── core/
│   ├── config.py
│   ├── jwt.py
│   ├── logging.py
│   ├── rate_limit.py
│   ├── redis.py
│   └── retryPolicy.py
│
├── db/
│   ├── base.py
│   └── models.py
│
├── middleware/
│   ├── jwtAuthMiddleware.py
│   ├── requestIDMiddleware.py
│   └── timeoutMiddleware.py
│
├── schemas/
│   ├── generate.py
│   └── __init__.py
│
├── services/
│   └── llm.py
│
├── utils/
│   ├── hash.py
│   ├── publicPaths.py
│   └── validate.py
│
├── main.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── pyproject.toml
├── requirements.txt
└── .env.example


frontend/
│
├── node_modules/
├── package-lock.json
├── package.json
├── postcss.config.js
├── public/
├── README.md
│
├── src/
│   ├── App.js
│   ├── authStore.js
│   ├── axios.js
│
│   ├── component/
│   │   ├── CommonIcons.jsx
│   │   ├── CreateSurvey.jsx
│   │   ├── CreateSurveyContent.jsx
│   │   ├── CreateSurveyProvider.jsx
│   │   ├── CreateSurveySidebar.jsx
│   │   ├── CreateSurveySteps.jsx
│   │   ├── DashboardLayout.jsx
│   │   ├── Header.jsx
│   │   ├── helper.jsx
│   │   ├── Icons.jsx
│   │   ├── QuestionItem.jsx
│   │   ├── QuestionList.jsx
│   │   ├── RenderCheckboxOptions.jsx
│   │   ├── RenderMultipleOptions.jsx
│   │   ├── Sidebar.jsx
│   │── getAuthToken.js
│   ├── index.css
│   ├── index.js
│
│   ├── pages/
│   │   └── CreateSurveyPage.jsx
│
├── tailwind.config.js


```

## Deployment

### Docker Deployment
```bash
docker-compose up --build -d
```

## Testing

### Running Tests
```bash
pytest tests/
```

### Test Coverage
Key test cases:
- Survey generation with valid input
- Cache hit scenarios
- Authentication failure cases
- Rate limiting enforcement
- Input validation checks
- Error handling for external services

## Frontend Integration

The React frontend integrates with the backend through:

1. **Generate Survey Button**  
   Added to CreateSurvey.jsx with AI generation logic

2. **API Client**  
   Uses Axios with interceptors for JWT handling

3. **State Management**  
   Zustand for auth state and CreateSurveyProvider for survey state

### Integration Flow
1. User clicks "Generate Survey" button
2. Frontend prompts for survey description
3. Axios POST request to `/api/surveys/generate`
4. Backend processes request and returns JSON
5. Frontend transforms and renders survey

## Bonus Features Implemented

1. **Dockerization**  
   - Complete Docker setup with compose
   - Multi-stage builds
   - Health checks for dependencies

2. **Rate Limiting**  
   - 10 requests/minute per IP
   - Custom error responses

3. **Authentication**  
   - JWT token-based auth
   - Token refresh handling
   - Role-based claims

4. **Caching Strategy**  
   - Redis as primary cache
   - PostgreSQL as persistent cache
   - Automatic cache invalidation

5. **Comprehensive Logging**  
   - Request IDs for tracing
   - Structured logging with Loguru
   - Error tracking

## Areas of Focus

1. **Prompt Engineering**  
   Carefully crafted system prompts ensure:
   - Consistent JSON output
   - Relevant question selection
   - Neutral and unbiased questions
   - Appropriate survey length (5-8 questions)

2. **Error Resilience**  
   - Retry policies for external services
   - Graceful degradation
   - Comprehensive error messages
   - Fallback mechanisms

3. **Performance Optimization**  
   - Async database operations
   - Connection pooling
   - Efficient prompt hashing
   - Minimal payload sizes

4. **Security Hardening**  
   - Input validation and sanitization
   - JWT signature verification
   - Rate limiting
   - CORS protection
   - Request timeouts

## Troubleshooting

### Common Issues
1. **Authentication Errors**  
   - Verify JWT_SECRET matches between services
   - Check token expiration time
   - Ensure Authorization header format: `Bearer <token>`

2. **LLM Generation Failures**  
   - Validate GROQ_API_KEY
   - Check Groq service status
   - Verify network connectivity to Groq API

3. **Database Connection Issues**  
   - Check PostgreSQL logs
   - Verify DATABASE_URL format
   - Ensure DB is accessible from backend

4. **Caching Problems**  
   - Check Redis connection
   - Verify TTL settings
   - Monitor cache hit/miss ratios

### Logs
View logs with:
```bash
docker-compose logs -f backend
```

## Acknowledgments

- Groq for providing powerful LLM inference
- FastAPI for the excellent web framework
- PostgreSQL and Redis for reliable data storage
- Boundary AI for the challenging task

## Future Improvements

- Cache token generation results
- Store payload as JSON in DB instead of string
- Semantic matching for similar survey prompts
- Alembic migrations
- Unit & integration tests
- Voice input for prompts
- Auto-generate trending surveys from real-world data
