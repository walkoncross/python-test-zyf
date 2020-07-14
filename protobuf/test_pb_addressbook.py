import sys
sys.path.insert(0, './compiled_protos')

import addressbook_pb2
from google.protobuf.json_format import MessageToJson


# init and set an object
person = addressbook_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.HOME

## test wrong attr
#person.no_such_field = 1  # raises AttributeError
## test wrong type
#person.id = "1234"        # raises TypeError

print '\n===> proto data'
print '-> type: ', type(person)
print '-> data: ', person

print '\n===> proto MessageToJson(person) string'
json_str = MessageToJson(person)
print '-> type: ', type(json_str)
print '-> string: ', json_str 
print '-> string length: ', len(json_str)

print '\n===> proto serialized string'
serialized_str = person.SerializeToString()
print '-> type: ', type(serialized_str)
print '-> string: ', serialized_str 
print '-> string length: ', len(serialized_str)

