from functools import wraps

def tags(tag_name):
    def tags_decorator(func):
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator

@tags("p")
def get_text(name):
    return "Hello "+name

print '===test decorator without wraps'

print get_text("John")

# Outputs <p>Hello John</p>

print get_text.func_name
# Outputs func_wrapper
print get_text.__name__ # get_text
print get_text.__doc__ # returns some text
print get_text.__module__ # __main__


print '\n===test decorator with wraps'

def tags_with_wraps(tag_name):
    def tags_decorator(func):
        @wraps(func)# without this get_text
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator

@tags_with_wraps("p")
def get_text2(name):
    return "Hello "+name

print get_text2("John")

# Outputs <p>Hello John</p>

print get_text2.func_name
# Outputs get_text2
print get_text2.__name__ # get_text2
print get_text2.__doc__ # returns some text
print get_text2.__module__ # __main__
