from pydantic import BaseModel


class MessageHistory(BaseModel):
    content: str
    timestamp: str
    sender: str
    receiver: str

    @classmethod
    def from_message(cls, messages):
        return [cls(
            content=message.content,
            timestamp=message.timestamp.strftime('%d.%m.%Y, %H:%M:%S'),
            sender=message.sender.username,
            receiver=message.receiver.username
        ) for message in messages]
