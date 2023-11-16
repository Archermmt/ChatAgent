import json
import requests


class BaseClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._url = "http://{}:{}".format(host, port)

    def setup(self, db_type, db_config=None, agent_config=None):
        # set up data bank
        data = {
            "task_type": "setup",
            "service_type": self.service_type,
            "db_type": db_type,
            "db_config": db_config or {},
            "agent_config": agent_config or {},
        }
        request = requests.post(self._url, data=json.dumps(data))
        return json.loads(request.text)

    def analysis(self, analysis_type, config=None):
        config = config or {}
        config["analysis_type"] = analysis_type
        data = {"task_type": "analysis", "config": config}
        request = requests.post(self._url, data=json.dumps(data))
        return json.loads(request.text)

    def chat(self, chat_type, config=None):
        config = config or {}
        config["chat_type"] = chat_type
        data = {"task_type": "chat", "config": config}
        request = requests.post(self._url, data=json.dumps(data))
        return json.loads(request.text)

    def exit(self):
        data = {"task_type": "exit"}
        request = requests.post(self._url, data=json.dumps(data))
        return json.loads(request.text)

    @property
    def service_type(self):
        raise NotImplementedError("Service_type is not implemented for BaseClient")
