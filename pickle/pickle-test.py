import pickle


class Person:
    def __init__(self, n, a):
        self.name = n
        self.age2 = a
        self.addr = ''

    def show(self):
        print "name: " + self.name + "\nage: " + str(self.age2)


# aa = Person("JGood", 2)
# aa.show()

# f = open('./p.txt', 'w')
# pickle.dump(aa, f, 0)
# f.close()

# del Person
f = open('./p.txt', 'r')
bb = pickle.load(f)
f.close()
bb.show()
