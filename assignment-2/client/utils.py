class Bytes:
  @staticmethod
  def from_str(str) -> bytes:
    return str.encode('utf-8')

  @staticmethod
  def to_str(bytes) -> str:
    return bytes.decode('utf-8')


class Message:
  @staticmethod
  def get_content(message: str) -> str:
    return message.split(':')[1]

  @staticmethod
  def create(user: str, message: str) -> str:
    return f'{user}:{message}'

  @staticmethod
  def create_greeting(user: str) -> str:
    return f'{user}:join the conversation!'

  @staticmethod
  def get_sender(message: str) -> str:
    return message.split(':')[0]

  @staticmethod
  def is_greeting(message: str) -> bool:
    return 'join the conversation' in message
