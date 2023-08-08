from fastapi import HTTPException
from starlette import status

from app.auth import crud, models, schemas
from app.auth.exceptions import EmailAlreadyTaken, UserNotFound
from app.common.deps import CurrentActiveUser, DBSession
from app.common.utils import validate_instance_id
from app.core.config import settings


def valid_user_id(db: DBSession, user_id: int) -> models.User:
    event = validate_instance_id(db, id_=user_id, crud_service=crud.user, not_found_exception=UserNotFound())
    return event


def validate_unique_email(db: DBSession, email: str) -> None:
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise EmailAlreadyTaken()


def user_update_unique_email(
    db: DBSession, current_user: CurrentActiveUser, user_in: schemas.UserUpdate
) -> schemas.UserUpdate:
    if user_in.email is not None and not current_user.email == user_in.email:
        validate_unique_email(db, email=str(user_in.email))
    return user_in


def user_create_unique_email(db: DBSession, user_in: schemas.UserCreateOpen) -> schemas.UserCreateOpen:
    validate_unique_email(db, email=str(user_in.email))
    return user_in


def open_registration_allowed() -> None:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(detail="Open registration is forbidden", status_code=status.HTTP_403_FORBIDDEN)
