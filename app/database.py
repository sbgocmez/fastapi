from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import pymysql

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:busra123@localhost/fastapi"

# SQLALCHEMY_DATABASE_URL = "postgresql://wxdrjneihowrax:postgres:busra123@localhost/fastapi"

#heroku
SQLALCHEMY_DATABASE_URL = "postgresql://tmajtewkwsfkod:675c05a502cabbb4cf76472bd0adf771bb38105804e9dc8511f7bd710dd8cbfb@ec2-44-218-92-155.compute-1.amazonaws.com:5432/df61pteg205dne"

# AWS
# db_endpoint = "mydb-api-mysql.cibbmu3dasbu.eu-north-1.rds.amazonaws.com"
# db_port = 3306  # Default MySQL port
# db_username = "admin"
# db_name = "mydatabase"
# db_password = "busra123"

# # Create the SQLAlchemy database URL
# db_url = f"mysql://{db_username}:{db_password}@{db_endpoint}:{db_port}/{db_name}"

# SQLALCHEMY_DATABASE_URL = db_url
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

