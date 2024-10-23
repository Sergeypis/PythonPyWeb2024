def decor(param=None):
    print(param)
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print("start")
            func(*args, **kwargs)
            print("finish")
        return wrapper
    return my_decorator


if __name__ == "__main__":
    @decor()
    def my_funk(data:str):
        print("'Hello'" + data)

    my_funk('1')


