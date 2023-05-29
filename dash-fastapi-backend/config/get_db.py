from config.database import *


def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    current_db = SessionLocal()
    try:
        yield current_db
    finally:
        current_db.close()


get_db = get_db_pro
