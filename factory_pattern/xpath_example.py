from src.auth.models import User
from src.auth.repository import XPathRepository


repository = XPathRepository("users.xml")


retrieved_user = repository.getByID("1")
print(retrieved_user.username) 

retrieved_user = repository.getByUsername("john.doe")
print(retrieved_user.email)

retrieved_user = repository.getByEmail("john.doe@example.com")
print(retrieved_user.username)