def log_response(response):
    if response.status_code == 200:
        print("Request successful!")
    else:
        print(f"Error! Status code: {response.status_code}")
