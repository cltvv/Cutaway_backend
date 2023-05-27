from uuid import uuid4

from src.image.unit_of_work import AbstractUnitOfWork

from src.image.models import Image


def create(image_uow: AbstractUnitOfWork, id: str, file_path: str):
    with image_uow:
        image_uow.images.add(Image(id, file_path))
        image_uow.commit()


def get(image_uow: AbstractUnitOfWork, id: str):
    with image_uow:
        image = image_uow.images.getByID(id)
        image_uow.commit()
    return image
    