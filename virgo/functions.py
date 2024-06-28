def default(*kwargs):
    return kwargs

def default_print(*args):
    print("Default passing args:", *args)
    return args

def get_default_return(data):
    def func():
        return data
    return func

def get_default_return_print(data):
    def func():
        print("returning data:", data.head())
        return (data,)
    return func

def get_copy_return_print(data):
    def func():
        print("returning data:", data.head())
        #TODO: check that this works
        return (data.copy(),)
    return func