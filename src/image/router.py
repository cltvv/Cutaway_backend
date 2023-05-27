from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import Annotated
import os
from uuid import uuid4
import shutil


from src.auth.models import User
from src.auth.router import get_current_user
from src.image.service import get, create

from src.image.unit_of_work import SqlAlchemyUnitOfWork

from src.config import ALLOWED_EXTENSIONS


router = APIRouter()


@router.post('')
def create_image(current_user: Annotated[User, Depends(get_current_user)], file: UploadFile = File(...)):

    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"

    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Invalid file extension. Only PNG, JPEG, and GIF are allowed"},
        )

    os.makedirs("uploads", exist_ok=True)

    image_path = os.path.join("uploads", filename)

    with open(image_path, "wb") as image_file:
        shutil.copyfileobj(file.file, image_file)
    
    file.file.close()

    id = uuid4()

    create(SqlAlchemyUnitOfWork(), id, image_path)

    return {"image_id": id}


def get_media_type(file_path: str):
    extension = file_path.split(".")[-1].lower()
    if extension == "png":
        return "image/png"
    elif extension == "jpeg" or extension == "jpg":
        return "image/jpeg"
    elif extension == "gif":
        return "image/gif"
    else:
        return None


@router.get('/{image_id}')
def get_image(image_id: str):

    image = get(SqlAlchemyUnitOfWork(), image_id)

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': 'Image not found'}
        )
    media_type = get_media_type(image.file_path)
    if media_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg': 'Invalid media type'}
        )
    return FileResponse(image.file_path, media_type=media_type)

    