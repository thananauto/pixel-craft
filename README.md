# pixel-craft

A production-ready Flask web application for optimizing JPEG, PNG, and WebP images with advanced controls and drag-and-drop upload functionality.

## Deployment strategy

This repository is best suited to a Docker-based deployment model. It includes a production Dockerfile, Gunicorn config, and a Compose file already prepared for that environment.

### Recommendation

Use a container host for production instead of deploying directly to Vercel serverless.

### Why not Vercel serverless?

The application currently assumes:
- a writable local `uploads/` directory
- a long-lived web process (Gunicorn)
- file cleanup in the app runtime
- native dependencies such as `python-magic` and OpenCV

These assumptions do not map cleanly to Vercel's serverless execution model, which is stateless and uses ephemeral filesystem storage.

## Requirements

- Python 3.11+
- Docker & Docker Compose
- Persistent storage for uploaded files

## Quick start

```bash
cp .env.example .env
# edit .env

docker compose up --build -d
```

Open:

```text
http://localhost:5000
```

## Production environment

Example environment variables:

```bash
SECRET_KEY=your-very-secure-random-string
FLASK_ENV=production
```

## Health check

```bash
curl http://localhost:5000/health
```

## Hosting providers

This app is compatible with any Docker-capable PaaS or VM, including:
- Render
- Railway
- Fly.io
- DigitalOcean App Platform
- self-hosted Docker on a VPS

## Related files

- `Dockerfile`
- `docker-compose.yml`
- `gunicorn.conf.py`
- `.env.example`

## Future serverless migration

A future Vercel deployment would require:
- object storage for uploaded files
- a replacement for in-memory rate limiting
- removal or externalization of `python-magic`/OpenCV
- a refactor away from the local filesystem workflow
