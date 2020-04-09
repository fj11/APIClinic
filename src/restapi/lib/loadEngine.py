
import time
import datetime
from .httplib import sendRequest
from threading import Thread

class Engine(Thread):
    def __init__(self, taskId, data, duration):
        Thread.__init__(self)
        self.taskId = taskId
        self.send_data = {
            "method": data["request_method__name"],
            "url": data["request_URL"],
            "headers": data["request_headers"],
            "body": data["request_body"],
            }
        self.duration = int(duration)
        self.result = {
            "id": data['id'],
            "response_code": {},
            "response_time": 0,
            "response_number": 0

        }
        self.response_code = {}
        self.response_time = 0
        self.response_number = 0
 
    def run(self):
        start_time = time.time()
    
        while time.time() - start_time < self.duration:
            try:
                response = sendRequest(**self.send_data)
                current_time = time.time()
                self.result['response_number'] += 1
                status = response.status_code
                if status not in self.result['response_code']:
                    self.result['response_code'][status] = 0
                self.result['response_code'][status]  += 1
                self.result['response_time'] = (current_time - start_time) / self.result['response_number']
            except:
                pass

def start(testcases, params):
    taskList = []
    duration = params['duration']
    clients = int(params['clients'])
    count = 1
    while count <= clients:
        for testcase in testcases:
            task = Engine(count, testcase, duration)
            task.start()
            # task.join()
            taskList.append(task)
            count += 1
    for task in taskList:
        task.join()
    table = {}
    for task in taskList:
        success = 0
        client_error = 0
        server_error = 0
        for code in task.result["response_code"].keys():
            if code >=200 and code < 300:
                success += task.result["response_code"][code]
            elif code >= 400 and code < 500:
                client_error += task.result["response_code"][code]
            elif code >= 500 and code < 600:
                server_error += task.result["response_code"][code]

        if task.result["id"] not in table:
            table[task.result["id"]] = {
                "2xx": 0,
                "4xx": 0,
                "5xx": 0,
                "response_number": 0,
                "response_time": task.result["response_time"]
            }
        table[task.result["id"]]["2xx"] += success
        table[task.result["id"]]["4xx"] += client_error
        table[task.result["id"]]["5xx"] += server_error
        table[task.result["id"]]["response_number"] += task.result["response_number"]
        table[task.result["id"]]["response_time"] = (  table[task.result["id"]]["response_time"] + task.result["response_time"]) / 2
    return table




