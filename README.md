# DevOps Demo Project — Serverless Form Submission

A demo project showcasing CI/CD pipeline implementation for a serverless application on AWS.

## Architecture

```
CloudFront → S3 (static website) → API Gateway → Lambda (Python)
```

## Project Structure

```
├── .github/workflows/       # CI/CD pipeline definitions
│   ├── ci.yml               # Continuous Integration (test + validate)
│   └── deploy.yml           # Continuous Deployment (deploy to AWS)
├── backend/
│   ├── lambda_function.py   # Lambda handler
│   ├── requirements.txt     # Python dependencies
│   └── tests/
│       └── test_handler.py  # Unit tests
├── frontend/
│   └── index.html           # Static website
└── README.md
```

## CI/CD Pipeline

**On every push:**
1. Lint Python code (flake8)
2. Run unit tests (pytest)
3. Package Lambda function
4. Deploy Lambda to AWS
5. Deploy frontend to S3
6. Invalidate CloudFront cache

## Technologies

- **CI/CD:** GitHub Actions
- **Backend:** AWS Lambda (Python 3.11)
- **Frontend:** Static HTML on S3 + CloudFront
- **IaC:** Terraform (planned)
- **Monitoring:** CloudWatch
