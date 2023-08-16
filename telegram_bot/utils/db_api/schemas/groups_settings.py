from utils.db_api.db_gino import TimeBaseModel
from sqlalchemy import Column, BigInteger, String, Boolean, sql, ColumnDefault, false

class Settings(TimeBaseModel):
    __tablename__ = 'chat_settings'
    chat_id = Column(BigInteger, primary_key=True)
    chat_name = Column(String(255))
    delete_link = Column(Boolean, ColumnDefault(bool(0)))
    delete_admins_link = Column(Boolean, ColumnDefault(bool(0)))

    query: sql.select 