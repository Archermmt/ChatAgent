class ChatService:
    SERVICES = {}


def register_service(name, cls):
    ChatService.SERVICES[name] = cls


def get_registered_service(name):
    return ChatService.SERVICES.get(name)
