import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"text": "what is python"},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nFull Response:")
    print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
