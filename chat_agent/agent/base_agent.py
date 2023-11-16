import logging


class BaseAgent:
    def __init__(self, data_bank, config=None):
        self.logger = logging.getLogger("agent")
        self._data_bank = data_bank
        self.setup(config)

    def __str__(self):
        return "Agent[{}]".format(self.__class__.__name__)

    def setup(self, config=None):
        raise NotImplementedError("setup is not implemented for BaseAgent")

    def analysis(self, analysis_type, config):
        if analysis_type == "update_table":
            for name, info in config["content"].items():
                self._data_bank.add_item(config["table"], name, info)
            return self._data_bank.get_table(config["table"])
        elif analysis_type == "get_table":
            return self._data_bank.get_table(config["table"])
        elif analysis_type == "get_friends":
            table_name, friends = self._get_friends(**config)
            for name, info in friends.items():
                self._data_bank.add_item(table_name, name, info)
            return friends
        elif analysis_type == "find_friend":
            for table in self._data_bank.get_tables():
                friend = self._find_friend(table, **config)
                if friend:
                    return friend
            return {}
        raise TypeError("Unexpected analysis_type " + str(analysis_type))

    def chat(self, chat_type, config):
        if chat_type == "send_msg":
            return self._send_message(**config)
        elif chat_type == "add_friend":
            return self._add_friend(**config)
        raise TypeError("Unexpected chat_type " + str(chat_type))

    def exit(self):
        self._data_bank.commit()

    def _get_friends(self, **kwargs):
        raise NotImplementedError("_get_friends is not implemented for BaseAgent")

    def _find_friend(self, table, **kwargs):
        raise NotImplementedError("_find_friend is not implemented for BaseAgent")

    def _send_message(self, **kwargs):
        raise NotImplementedError("_send_message is not implemented for BaseAgent")

    def _add_friend(self, **kwargs):
        raise NotImplementedError("_add_friend is not implemented for BaseAgent")
