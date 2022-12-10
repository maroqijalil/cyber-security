from datetime import datetime


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


class Request:
  @staticmethod
  def generate(id_a = 'ID-A', id_b = 'ID-B'):

    current_time = datetime.now()
    current_time = current_time.ctime()

    return f'{id_a};{id_b};{current_time}', current_time

  @staticmethod
  def validate_time(request: str, time: str):
    request = request.split(';')[-1]

    return request == time
