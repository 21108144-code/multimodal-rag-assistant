# Demo Requests

## Text Query
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is in the image?"}'
```

## Image Query
```bash
curl -X POST "http://localhost:8000/query/image" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/image.jpg"
```

## Health Check
```bash
curl http://localhost:8000/health
```
