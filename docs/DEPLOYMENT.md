# Deployment and CI for SAMMO Fight IQ

This document shows how to deploy the Cloud Function and explains the included GitHub Actions workflow.

## Local deployment (gcloud)

1. Authenticate and set project:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. (Optional) Create a service account for Cloud Functions deployment and grant `roles/cloudfunctions.developer` and `roles/iam.serviceAccountUser`.

3. Deploy the function:

```bash
gcloud functions deploy sammo \
  --entry-point=sammo \
  --runtime=python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region=us-central1 \
  --source=.
```

Notes:
- The function entry point is `sammo` (in `main.py`).
- The function uses Firestore; ensure Firestore is enabled in the project and appropriate IAM roles are granted.

## GitHub Actions CI & (optional) Deploy

There is a workflow at `.github/workflows/ci.yml` that runs on push and PRs.

- It installs dependencies from `requirements.txt` and runs `pytest`.
- If you provide the repository secrets `GCP_CREDENTIALS` (JSON key) and `GCP_PROJECT`, the workflow will authenticate and deploy the function automatically when pushing to `main`.

How to set secrets:

1. Create a service account in the GCP Console and generate a JSON key.
2. Add the JSON contents as the `GCP_CREDENTIALS` secret in GitHub repo Settings → Secrets.
3. Add `GCP_PROJECT` with your project id.

Security note: Keep the service-account key secret and scope the account to the minimum required roles.
