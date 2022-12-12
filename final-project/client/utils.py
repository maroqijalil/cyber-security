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
  def create_farewell(user: str) -> str:
    return f'{user}:left the conversation!'

  @staticmethod
  def create_exchange(user: str, message: str) -> str:
    return f'exchange:{user};{message}'

  @staticmethod
  def get_sender(message: str) -> str:
    return message.split(':')[0]

  @staticmethod
  def is_greeting(message: str) -> bool:
    return 'join the conversation' in message

  @staticmethod
  def is_farewell(message: str) -> bool:
    return 'left the conversation' in message

  @staticmethod
  def is_exchange(message: str) -> bool:
    return message.split(':')[0] == 'exchange'


class Request:
  @staticmethod
  def create_set(id: str, key: str):
    return f'set {id};{key}'

  @staticmethod
  def create_get(id_a, id_b):
    current_time = datetime.now()
    current_time = current_time.ctime()

    return f'get {id_a};{id_b};{current_time}'
  
  @staticmethod
  def validate_from_get(response: str, request: str):
    responses = response.split(';')
    requests = request.split(' ')

    if ((';').join(responses[1:]) == (' ').join(requests[1:])):
      return responses[0]
    
    return None

  @staticmethod
  def validate_time(request: str, time: str):
    request = request.split(';')[-1]

    return request == time
