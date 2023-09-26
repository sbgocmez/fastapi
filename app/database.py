from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:busra123@localhost/fastapi"

# SQLALCHEMY_DATABASE_URL = "postgresql://wxdrjneihowrax:postgres:busra123@localhost/fastapi"

SQLALCHEMY_DATABASE_URL = "postgresql://wxdrjneihowrax:fd620896e4bec3696b5e48b8cd943f53d5374c553e176bf6ef1a68ceefeb62b1@ec2-52-205-171-232.compute-1.amazonaws.com:5432/d397m5f10p3vj7"

# 'postgresql://<username>:<password>@ip-address/hostname/<databasename>'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# get our database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

