from repository_factory import UserRepositoryFactory


factory = UserRepositoryFactory()
repository = factory.get_repository('JSON')
user = repository.getByID('1')
print(user.email)

repository = factory.get_repository('XML')
user = repository.getByID('1')
print(user.email)