import itchat

if __name__ == "__main__":
    itchat.auto_login()
    print("login done!!")
    chatroom_name = "幸福"
    chatrooms = itchat.search_chatrooms(chatroom_name)
    print("chatrooms " + str(chatrooms))
    chatroom_name = itchat.search_chatrooms(chatroom_name)[0]["UserName"]
    print("chatroom_name " + str(chatroom_name))
    itchat.send(msg="群消息自动发送", toUserName=chatroom_name)

    """
    friends = itchat.get_friends()
    for friend in friends:
        print("has friend " + str(friend))
    chatrooms = itchat.get_chatrooms()
    for chatroom in chatrooms:
        print(chatroom["NickName"], chatroom["UserName"])
    print("check menbers")
    chatroom_name = "认证成功"
    chatrooms = itchat.search_chatrooms(chatroom_name)
    print("chatrooms of 2 " + str(chatrooms))
    if chatrooms:
        chatroom = itchat.update_chatroom(chatrooms[0]["UserName"])
        for member in chatroom["MemberList"]:
            print(member["NickName"], member["UserName"])
    """
    # send message
    target = itchat.search_friends(name="Archer")[0]["UserName"]
    print("target " + str(target))
    itchat.send("测试", toUserName=target)
