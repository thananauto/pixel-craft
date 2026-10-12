# pixel-craft deployment guide

This project is designed to run as a long-lived Flask application with a writable `uploads/` directory and native Python dependencies. For that reason, it is best deployed on a Docker-capable host rather than directly on Vercel serverless.

## Recommended deployment model

Use one of the following:
- Render, Railway, Fly.io, DigitalOcean App Platform
- Docker hosts such as any VM with Docker installed
- Kubernetes or ECS with a persistent volume

Why this is the best fit:
- The app persists processed files in the local `uploads` directory (`UPLOAD_FOLDER` in `config.py`)
- It uses `python-magic` and OpenCV, which are not a typical serverless fit
- It relies on a long-lived Gunicorn process, not a stateless function invocation model

## Prerequisites

- Docker Engine
- Docker Compose (optional but recommended)
- A persistent volume or mounted directory for `/app/uploads`
- A secure `SECRET_KEY`

## Environment variables

Set these in your deployment environment or in a `.env` file:

```bash
SECRET_KEY=replace-with-a-long-random-secret
FLASK_ENV=production
```

## Local production-style deployment with Docker Compose

```bash
cp .env.example .env
# edit .env with your values

docker compose up --build -d
```

Then verify:

```bash
curl http://localhost:5000/health
```

The included `docker-compose.yml` mounts a Docker volume at `/app/uploads`, which keeps uploaded files available while the container is running.

## Deploying to a container host

For a managed platform, most services will follow the same pattern:

1. Build the image from the repo's `Dockerfile`
2. Expose port `5000`
3. Set `SECRET_KEY` and `FLASK_ENV`
4. Mount a persistent volume at `/app/uploads`
5. Start the container with the default command:

```bash
gunicorn --config gunicorn.conf.py app:app
```

## Important production notes

- Do not rely on ephemeral filesystem storage for uploaded images.
- Keep the `uploads` directory mounted to a persistent volume.
- Keep `DELETE_AFTER_RESPONSE=true` only if you want temporary files to be cleaned immediately after download.
- If you need a serverless deployment later, the app will need a refactor to move upload storage to object storage and replace or externalize native image-processing dependencies.

## Vercel note

This repository is not a direct Vercel serverless app. A Vercel deployment would require:
- external file storage instead of the local `uploads` directory
- a managed rate-limiter backend instead of `memory://`
- a replacement for `python-magic` and/or a removal of OpenCV-based processing
- a re-architecture for uploads, previews, and cleanup

For now, Docker-based hosting is the recommended path.
