from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# URL_DATABASE = "mysql+mysqlconnector://<username>:<password>@<host>/<database>"
URL_DATABASE = "mysql+mysqlconnector://root:!Tawfiqrq1998@localhost:3306/price_benchmark"
connect_args = {"check_same_thread": False}



engine=create_engine(URL_DATABASE)
meta= MetaData()
connection=engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()