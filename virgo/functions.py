def default(*kwargs):
    return kwargs

def default_print(*kwargs):
    print(kwargs)
    return kwargs

def get_default_return(data):
    def func():
        return data
    return func

def get_default_return_print(data):
    print("returning data")
    def func():
        return data
    return func