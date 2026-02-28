from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/ecommerce'
engine = create_engine(URL_DATABASE)
sessionLocal=sessionmaker(autoflush=False, autocommit=False,bind=engine)
Base=declarative_base()
