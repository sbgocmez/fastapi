from .database import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# database table look
class Track(Base):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True, nullable=False)
    device = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    
    # timestamp will be added
    
class Visit(Base):
    __tablename__ = "Visits"
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    device = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

