from datetime import datetime


def job(*args, **kwargs):
    print(args[0])
    print(kwargs)
    print(f"{datetime.now()}执行了")