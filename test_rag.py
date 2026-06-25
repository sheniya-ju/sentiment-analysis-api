import requests

# Test 1 - Upload document
with open(r"C:\Users\Sheniya\Desktop\test_document.txt", "rb") as f:
    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files={"file": ("test_document.txt", f, "text/plain")}
    )
print("UPLOAD RESPONSE:")
print(response.json())

# Test 2 - Ask a question
response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "What is RAG?"}
)
print("\nASK RESPONSE:")
print(response.json())