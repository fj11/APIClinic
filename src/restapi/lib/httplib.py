
import requests

def sendRequest(**params):

    method = params.get("method", "")
    url = params.get("url", "")
    headers = params.get("header", {})
    body = params.get("body", {})
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers = headers, data=body)
    elif method == "PUT":
        response = requests.put(url, data=body)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, data=body)

    return response
