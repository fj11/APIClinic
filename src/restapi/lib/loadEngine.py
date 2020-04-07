
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
    return [task.result for task in taskList]


