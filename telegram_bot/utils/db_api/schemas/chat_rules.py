from utils.db_api.db_gino import TimeBaseModel
from sqlalchemy import Column, BigInteger, String, sql

class Chat_rules(TimeBaseModel):
    __tablename__ = 'chat_rules'
    chat_id = Column(BigInteger, primary_key=True)
    rules = Column(String(1024))
    
    query: sql.select 