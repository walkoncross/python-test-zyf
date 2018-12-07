import easydict

global_var = 1
global_dict = {'a': 1, 'b': 2}


class Base:
    def __init__(self, a=0, b=1):
        self.a = a
        self.b = b
        print global_var

    def __init__(self):
        self.a = global_dict['a']
        self.b = global_dict['b']
        print global_dict

    def __init__(self, loacl_dict):
        self.a = loacl_dict['a']
        self.b = loacl_dict['b']
        print loacl_dict

    def sum(self):
        print self.a + self.b


def main():
    global_var = 2

    inst_a = Base()
    inst_a.sum()

    local_dict = global_dict
    print local_dict
    print global_dict

    inst_b = Base()
    inst_b.sum()

    local_dict['a'] = 3
    print local_dict
    print global_dict

    inst_c = Base()
    inst_c.sum()


def dict_test(dict_a):
    dict_a['age'] = 2
    print dict_a


main()


# dict_a = {'name': 'zyf', 'age': 31}
# print dict_a
# dict_test(dict_a)
# print dict_a
