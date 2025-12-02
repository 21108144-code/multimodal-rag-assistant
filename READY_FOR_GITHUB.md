# Ready for GitHub Checklist

Use this checklist to verify the repository is fully functional before pushing or demonstrating.

## 1. Setup
- [ ] **Install Dependencies**: Run `make setup`
- [ ] **Environment**: Check `requirements.txt` is installed.

## 2. Testing
- [ ] **Unit Tests**: Run `make test`. Ensure all pass.
- [ ] **Linting**: Run `make lint`. Ensure no errors.

## 3. Local Execution
- [ ] **Run API**: Run `make run-api`.
- [ ] **Health Check**: Visit `http://localhost:8000/health`.
- [ ] **Docs**: Visit `http://localhost:8000/docs`.

## 4. Docker
- [ ] **Build Image**: Run `make build`.
- [ ] **Run Container**: Run `docker run -p 8000:8000 multimodal-rag:latest`.

## 5. Demo
- [ ] **Ingest Data**: (Optional) Run `python src/data/ingest.py` with sample data.
- [ ] **Query**: Use the Swagger UI to send a test query.

## 6. Documentation
- [ ] **README**: Verify badges and links render correctly.
- [ ] **Architecture**: Check the Mermaid diagram.
