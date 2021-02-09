from data.MongoDB_MongoEngine.models.chats import Chat


def initiate_chat(user_1, user_2):
    chat = Chat(members=[user_1, user_2], messages=[])
    chat.save()
    user_1.chats.append(chat)
    user_1.save()
    user_2.chats.append(chat)
    user_2.save()


def get_all_chats():
    return [chat for chat in Chat.objects]


def get_chat_by_id(id):
    return Chat.objects.get(id=id)


def get_chat_between_users(user, friend):
    for chat in user.chats:
        if user and friend in chat.members:
            return chat


def add_message_to_chat(chat, message):
    chat.messages.append(message)
    chat.save()


def remove_user_chats(user):
    for chat in Chat.objects:
        if user in chat.members:
            chat.delete()
        chat.save()