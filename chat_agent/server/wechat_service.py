from chat_agent.agent import WeChatAgent
from chat_agent.utils.register import register_service
from .base_service import BaseService


class WeChatService(BaseService):
    def setup_agent(self, data_bank, config):
        return WeChatAgent(data_bank, config)


register_service("wechat", WeChatService)
