import json
from http.server import BaseHTTPRequestHandler

from chat_agent.databank import LocalDataBank
from chat_agent.utils.register import get_registered_service


class GlobalService:
    service = None


class BaseService:
    def __init__(self, db_type, db_config=None, agent_config=None):
        self._data_bank = self.setup_db(db_type, db_config)
        self._agent = self.setup_agent(self._data_bank, agent_config)

    def setup_agent(self, data_bank, config):
        raise NotImplementedError("setup_agent is not implemented!!")

    def setup_db(self, db_type, config):
        if db_type == "local":
            return LocalDataBank(config)
        raise TypeError("databank type {} is not supported".format(db_type))

    def __str__(self):
        return "Agent:{}, DB: {}".format(self._agent, self._data_bank)

    def analysis(self, config):
        if not self._agent:
            return {"success": False, "Error": "Please setup befor analysis"}
        assert "analysis_type" in config, "analysis_type should be given for analysis"
        analysis_type = config.pop("analysis_type")
        return self._agent.analysis(analysis_type, config)

    def chat(self, config):
        if not self._agent:
            return {"success": False, "Error": "Please setup befor chat"}
        assert "chat_type" in config, "chat_type should be given for chat"
        chat_type = config.pop("chat_type")
        return self._agent.chat(chat_type, config)

    def exit(self):
        self._agent.exit()

    @classmethod
    def create_service(cls, db_type, db_config=None, agent_config=None):
        GlobalService.service = cls(db_type, db_config, agent_config)

    @property
    def data_bank(self):
        return self._data_bank

    @property
    def agent(self):
        return self._agent


class BaseAgentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.write_response("do_GET is not supported")

    def get_service(self):
        return GlobalService.service

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)
        info = json.loads(body)
        task_type = info["task_type"]
        if task_type == "setup":
            if self.get_service():
                response = {"success": True, "agent": str(self.get_service())}
            else:
                service_cls = get_registered_service(info["service_type"])
                service_cls.create_service(
                    info["db_type"], info.get("db_config"), info.get("agent_config")
                )
                response = {"success": True, "agent": str(self.get_service())}
        elif task_type == "analysis":
            response = self.get_service().analysis(info["config"])
        elif task_type == "chat":
            response = self.get_service().chat(info["config"])
        elif task_type == "exit":
            response = self.get_service().exit()
        else:
            raise TypeError("Unexpected task_type " + str(task_type))
        self.write_response(json.dumps(response).encode("utf-8"))

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)
