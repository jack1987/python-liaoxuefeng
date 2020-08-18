
def add_routes(module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    print(mod)
    print(mod.__dict__)

add_routes('test')
add_routes('app.handle')
