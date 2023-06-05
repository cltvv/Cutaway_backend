from uuid import uuid4
from src.auth.models import User

user = User(uuid4, '123', '123@mail.ru', '123')


print(user.current_state)

user.send('block')

print(user.current_state)

user.send('activate')

print(user.current_state)

user.send('unblock')

print(user.current_state)

user.send('deactivate')

print(user.current_state)
