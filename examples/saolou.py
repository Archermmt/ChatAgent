"""Start server by python -m chat_agent.server.start_agent"""

from chat_agent.client import WeChatClient

if __name__ == "__main__":
    client = WeChatClient("localhost", 8080)
    my_friends = client.analysis("get_friends")
    src_chatroom = "志愿者们"
    dst_chatroom = "认证成功2号楼"
    src_friends = client.analysis("get_friends", config={"chatroom": src_chatroom})
    dst_friends = client.analysis("get_friends", config={"chatroom": dst_chatroom})
    # add friend or send message
    non_registered = client.analysis("get_table", config={"table": "non_registered"})
    black_list = client.analysis("get_table", config={"table": "black_list"})
    add_message = "您好，请加微信，我们会帮助您认证北京业主app"
    remind_message = "您好，请下载并注册业主app，若您已经在【{}】，请忽略此消息".format(dst_chatroom)
    registered = len([k for k in src_friends if k in dst_friends])
    final_message = "本群业主已认证 {}/{}, 认证率 {:g}%，未认证业主: ".format(
        registered, len(src_friends), float(registered) * 100 / len(src_friends)
    )
    for k, info in src_friends.items():
        nick = info["NickName"]
        if k in dst_friends:
            if k in non_registered:
                non_registered.pop(k)
                print("【{}】为新认证业主，移除记录".format(nick))
            elif k in black_list:
                black_list.pop(k)
                print("【{}】已悔过自新，移出黑名单".format(nick))
            else:
                print("【{}】已经在认证业主群，跳过注册".format(nick))
            continue
        if k in black_list or nick in black_list:
            print("【{}】在黑名单中，跳过".format(nick))
        if k not in my_friends:
            final_message = final_message + "@" + nick + " "
            if k not in non_registered:
                non_registered[k] = info
            if "add_cnt" not in non_registered[k]:
                non_registered[k]["add_cnt"] = 0
            print(
                "【{}】不是朋友, 已添加 {} 次: {}".format(
                    nick, non_registered[k]["add_cnt"], add_message
                )
            )
            non_registered[k]["add_cnt"] += 1
            if non_registered[k]["add_cnt"] > 10:
                black_list[k] = info
                black_list[k]["failed_reason"] = "{} 拒不加朋友, 后期重点攻克".format(nick)
                print(black_list[k]["failed_reason"])
        else:
            client.chat("send_msg", config={"nick": nick, "message": remind_message})
            if k not in non_registered:
                non_registered[k] = info
            if "remind_cnt" not in non_registered[k]:
                non_registered[k]["remind_cnt"] = 0
            print(
                "【{}】为已添加朋友, 已提醒 {} 次: {}".format(
                    nick, non_registered[k]["remind_cnt"], remind_message
                )
            )
            non_registered[k]["remind_cnt"] += 1
            if non_registered[k]["remind_cnt"] > 10:
                black_list[k] = info
                black_list[k]["failed_reason"] = "{} 拒不认证, 后期重点攻克".format(nick)
                print(black_list[k]["failed_reason"])

    final_message = final_message + "为支持小区业委会成立，请未认证的业主下载并认证业主app，注册过程若有疑问请加我微信"
    client.chat("send_msg", config={"chatroom": src_chatroom, "message": final_message})
    client.analysis(
        "update_table", config={"table": "non_registered", "content": non_registered}
    )
    client.analysis(
        "update_table", config={"table": "black_list", "content": black_list}
    )
    client.exit()
