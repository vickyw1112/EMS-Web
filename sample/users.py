from csv import DictReader


def createUser(row):
    return {
        'email': row['email'],
        'name': row['name'],
        'password': row['password'],
        'description': ''
    }


users = []

reader = DictReader(open('sample/sampleUsers.csv', "r"))
for row in reader:
    users.append(createUser(row))
