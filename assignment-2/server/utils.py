class Bytes:
  @staticmethod
  def from_str(str) -> bytes:
    return str.decode('utf-8')

  @staticmethod
  def to_str(bytes) -> str:
    return bytes.encode('utf-8')


class Message:
  @staticmethod
  def get_content(message: str) -> str:
    return message.split(':')[1][1:]

  @staticmethod
  def create(user: str, message: str) -> str:
    return f'{user}:{message}'
