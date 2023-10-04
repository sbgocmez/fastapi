from ..database import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
#import pymysql

class Client(Base):
    __tablename__ = "Clients2"
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(64), nullable=False)
    device = Column(String(32), nullable=False)
    platform = Column(String(32), nullable=False)
    language = Column(String(32), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))