import datetime
import sqlalchemy as sa
from aiogram import Dispatcher
from typing import List
from gino import Gino
from data import config

db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_colums: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[sa.column.name])
            for column in primary_key_colums
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now())

async def on_startup(dispatcher: Dispatcher):
    print('Встановлення зв\'язку з PostgresSQL')
    await db.set_bind(config.POSTGERS_URI)