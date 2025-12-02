import argparse
import uvicorn
from src.config import settings

def run_api():
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)

def run_ingest():
    from src.data.ingest import ingest_data
    ingest_data()

def main():
    parser = argparse.ArgumentParser(description="Multimodal RAG CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    api_parser = subparsers.add_parser("api", help="Run the API server")
    ingest_parser = subparsers.add_parser("ingest", help="Run data ingestion")
    
    args = parser.parse_args()
    
    if args.command == "api":
        run_api()
    elif args.command == "ingest":
        run_ingest()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
