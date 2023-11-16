"""Start server by python -m chat_agent.server.start_agent"""

from chat_agent.client import WeChatClient
import itchat

if __name__ == "__main__":
    client = WeChatClient("localhost", 8080)
    client.setup("local", {"path": "saolou_record"})

    itchat.send(
        "测试",
        toUserName="@3d1a31f412fade6d0fd526baf2e18ed4e0f31c58f1b0e3c56c7c679254fde03d",
    )
    raise Exception("stop here!!")

    my_friends = client.analysis("get_friends")
    src_friends = client.analysis("get_friends", config={"chatroom": "志愿者们"})
    dst_friends = client.analysis("get_friends", config={"chatroom": "认证成功2号楼"})
    me = client.analysis("find_friend", config={"nick": "Archer"})
    # client.chat("send_msg", config={"target": me["UserName"], "message": "test"})
    print("me " + str(me))
    itchat.send("test")
    print("message send!!")
    raise Exception("stop here!!")

    left_members = {}
    members_to_add = [k for k in src_friends if k not in dst_friends]
    for k in members_to_add:
        if k in my_friends:
            print("should send msg {}:{}".format(k, src_friends[k]))
        else:
            print("should add {}:{}".format(k, src_friends[k]))

    me = my_friends["08c458192aef73980985963a565fb4ae0ad5996b6bb871a3c4bbed52a4d4bd23"]
    print("me " + str(me))
    # client.chat("send",config={"target":k, "message":})

    client.exit()
