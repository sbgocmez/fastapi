from ..database import Base
from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
#import pymysql

class Visit(Base):
    __tablename__ = "Visits"
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    client_id = Column(Integer, ForeignKey("Clients.id", ondelete="CASCADE"), nullable=False)