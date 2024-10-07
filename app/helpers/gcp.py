from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

db = firestore.Client(project="boreal-sweep-437919-s1")

user1 = {
  "first": "Ada", 
  "last": "Lovelace", 
  "born": 1815
}

user2 = {
  "first": "Ada", 
  "last": "Lovelace", 
  "born": 1815
}

doc_ref = db.collection("users").document("alovelace")
doc_ref.set(user1)

doc_ref = db.collection("users").document("aturing")
doc_ref.set(user2)

users_ref = db.collection("users")
docs = users_ref.stream()

def view_users():  
  for doc in docs:
      print(f"{doc.id} => {doc.to_dict()}")