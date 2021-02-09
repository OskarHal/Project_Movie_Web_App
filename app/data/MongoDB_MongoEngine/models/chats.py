from mongoengine import ListField, Document, EmbeddedDocumentListField, ReferenceField

from data.MongoDB_MongoEngine.models.messages import Message


class Chat(Document):
    members = ListField(ReferenceField('User'))
    messages = EmbeddedDocumentListField(Message)

    def __str__(self):
        return f"Members: {self.members} - Messages: {self.messages}"
