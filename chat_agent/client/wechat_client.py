from .base_client import BaseClient


class WeChatClient(BaseClient):
    @property
    def service_type(self):
        return "wechat"
