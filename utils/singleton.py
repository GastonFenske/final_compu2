class SingletonPattern():    

    @staticmethod
    def singleton(cls):
        # print('ya se creo una vez', cls)
        instances = dict()
        def wrapper(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return wrapper
