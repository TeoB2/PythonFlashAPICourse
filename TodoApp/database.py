from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" #sqlite
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Formula1?@localhost/TodoApplicationServer" #postgres - lovalhost
SQLALCHEMY_DATABASE_URL = "postgresql://matteo:W9a1HBZ3erh6emjSY6mJOGfc5rs9rBgN@dpg-cscmf1jqf0us73eorjbg-a.frankfurt-postgres.render.com/pythonflashapicourse" #postgres - render
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Formula1?@127.0.0.1:3306/TodoApplicationServer" #mysql

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) #sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL) #postgres
#engine = create_engine(SQLALCHEMY_DATABASE_URL) #mysql


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
