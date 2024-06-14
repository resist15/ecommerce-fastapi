from fastapi import APIRouter
from models import *
from core.hashing import Hash

router = APIRouter(
    tags=['Registration']
)


@router.post('/registration')
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = Hash.bcrypt(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status": 'ok',
        'data': f'Hello {new_user.username}, thanks for using our services. Please check your email inbox'
    }
