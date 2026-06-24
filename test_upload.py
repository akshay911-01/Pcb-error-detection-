import requests

try:
    response = requests.post("http://127.0.0.1:8000/predict", files={"file": ("dummy.jpg", b"fake binary data", "image/jpeg")})
    print(response.status_code)
    print(response.text)
except Exception as e:
    print("Failed with:", e)
