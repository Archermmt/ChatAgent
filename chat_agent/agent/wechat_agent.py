import itchat

from .base_agent import BaseAgent


class WeChatAgent(BaseAgent):
    def setup(self, config):
        itchat.auto_login()

    def _get_friends(self, chatroom=None):
        if chatroom:
            chatrooms = itchat.search_chatrooms(chatroom)
            self.logger.info("Chatrooms of {}: {}".format(chatroom, chatrooms))
            if chatrooms:
                c_room = itchat.update_chatroom(chatrooms[0]["UserName"])
                friends = {m["UserName"]: dict(m) for m in c_room["MemberList"]}
                return c_room["NickName"], friends
            return "Non-chatroom", {}
        friends = {f["UserName"]: dict(f) for f in itchat.get_friends()}
        return "friends", friends

    def _find_friend(self, table, id=None, nick=None):
        if not table:
            return {}
        if id:
            return table[id]
        if nick:
            for info in table.values():
                if info["NickName"] == nick:
                    return info
        return {}

    def _send_message(self, message, name=None, nick=None, chatroom=None):
        if chatroom:
            chatroom_id = itchat.search_chatrooms(chatroom)[0]["UserName"]
            self.logger.info("Send to chatroom {}({})".format(chatroom, chatroom_id))
            itchat.send(msg=message, toUserName=chatroom_id)
        elif name:
            self.logger.info("Send to " + str(name))
            itchat.send(msg=message, toUserName=name)
        elif nick:
            name = itchat.search_friends(name=nick)[0]["UserName"]
            self.logger.info("Send to {}({})".format(nick, name))
            itchat.send(msg=message, toUserName=name)
        else:
            raise Exception
        return {}

    def _add_friend(self):
        raise NotImplementedError("_add_friend is not implemented for BaseAgent")
