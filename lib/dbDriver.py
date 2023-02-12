import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)



#insert into Firebase
def insert():
    print("hello")

#delete from Firebase
def delete():
    print("hello")


