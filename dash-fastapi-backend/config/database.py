from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.env import DataBaseConfig

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DataBaseConfig.USERNAME}:{DataBaseConfig.PASSWORD}@" \
                          f"{DataBaseConfig.HOST}:{DataBaseConfig.PORT}/{DataBaseConfig.DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
