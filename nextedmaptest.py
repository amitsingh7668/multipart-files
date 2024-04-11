# Sample BusinessObject class
from wholeflow import generate_dat
class BusinessObject:
    def __init__(self, details=None):
        self.details = details

class Details:
    def __init__(self, contacts=None):
        self.contacts = contacts

class Contacts:
    def __init__(self, email=None):
        self.email = email

# Function to update nested attribute based on nested key
def update_nested_attribute(obj, nested_key, value):
    keys = nested_key.split('_NEXTOBJECT_')
    current_obj = obj
    for key in keys[:-1]:
        current_obj = getattr(current_obj, key)
    setattr(current_obj, keys[-1], value)

# Example usage
# Create a sample BusinessObject with nested structure

# Sample key-value pair
key = 'details_NEXTOBJECT_contacts_NEXTOBJECT_email'
value = 'bob@example.com'

datalis = generate_dat()

# Update the nested attribute using the key-value pair
listobj = []
for dat in datalis:
    business_obj = BusinessObject(Details(Contacts()))
    for key, value in dat.items():
        update_nested_attribute(business_obj, key, value)
    listobj.append(vars(business_obj))

print(listobj)



