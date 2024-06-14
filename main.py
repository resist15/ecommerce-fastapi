from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from api.routes import registration
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from models import *

app = FastAPI()


@post_save(User)
async def create_business(
        sender: 'Type[User]',
        instance: User,
        created: bool,
        using_db: Optional[BaseDBAsyncClient],
        update_fields: List[str]
) -> None:
    if created:
        business_obj = await Business.create(
            business_name=instance.username,
            owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)


register_tortoise(
    app,
    db_url='sqlite://database.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(registration.router)
