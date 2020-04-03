
import datetime
from .httplib import sendRequest

def start(data):
    send_data = {
        "method": data["request_method__name"],
        "url": data["request_URL"],
        "headers": data["request_headers"],
        "body": data["request_body"]
    }
    startTime = datetime.datetime.now()
    response = sendRequest(**send_data)
    result = "PASS" if isValid(response, data) else "FAILED"
    return {
        "id" : data["id"],
        "result": result,
        "reason": "",
        "real_status": response.status_code,
        "real_response": response.content,
        "duration": datetime.datetime.now()-startTime
    }

def isValid(response, data):
    status_code, content = response.status_code, response.content
    return codeValidation(status_code, data["expected_response"]) and stringValidation(content, data["expected_data"])

def codeValidation(response_code, expected_code):
    if expected_code == "":
        return True
    return response_code == expected_code

def dataValidation(response_data, expected_data):
    return stringValidation(response_data, expected_data) or keyValueValidation(response_data, expected_data)

def stringValidation(response_data, expected_data):
    if expected_data == "":
        return True
    return response_data == expected_data

def keyValueValidation(response_data, expected_data):

    keys, value = expected_data.split("=",1)
    keysList = keys.split(".")

    def helper(node, array):

        if isinstance(node, list):
            for i in node:
                return helper(i, array)
        key = array.pop(0)
        if key not in node:
            return False
        node = node[key]
        if array == []:
            return str(node) == str(value)
        else:
            return helper(node, array)
    return helper(response_data, keysList)


