from google.cloud import firestore
import datetime
# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

# Create doc
doc_ref = db.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})

# Upsert with merge
doc_ref.set({
    u'born': 1913
}, merge=True)

# Add server timestamp
doc_ref.update({
    'born': 1912,
    'timestamp': firestore.SERVER_TIMESTAMP
})

# Create autogenerate document ID and following doc
new_people_doc = db.collection(u'users').document()
new_people_doc.set({
    'first': 'Arthur',
    'middle': 'Camille',
    'last': 'Mauvezin',
    'born': 1993,
    'age': datetime.datetime.now().year - 1993,
    'likes': [
        'rugby',
        'games'
    ]
})

# Add values in array if not present
new_people_doc.update({
    'likes': firestore.ArrayUnion([
        'piano',
        'rugby',
        'loosing'
    ])
})

# Remove values from array
new_people_doc.update({
    'likes': firestore.ArrayRemove([
        'loosing'
    ])
})

# Increment field number
new_people_doc.update({
    'age': firestore.Increment(1)
})

# Delete field from doc
new_people_doc.update({
    'born': firestore.DELETE_FIELD
})

users_ref = db.collection(u'users')
docs = users_ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# Transaction example
transaction = db.transaction()

@firestore.transactional
def update_in_transaction(transaction, people_ref):
    snapshot = people_ref.get(transaction=transaction)
    new_age = snapshot.get(u'age') + 1
    if new_age < 30:
        transaction.update(people_ref, {
            'age': new_age
        })
        return True
    else:
        return False

result = update_in_transaction(transaction, new_people_doc)
if result:
    print(u'Good for the moment')
else:
    print(u'Sorry! You are too old.')

# Batch example
batch = db.batch()
batch.update(new_people_doc, {'height': 175})

doc_to_delete_ref = db.collection('users').document('todel')
batch.set(doc_to_delete_ref, {'todelete': True})

batch.delete(doc_to_delete_ref)
batch.commit()

# Delete document
new_people_doc.delete()

# Delete a collection content
# Whenever a collection is empty it is deleted
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

users_ref = db.collection(u'users')
delete_collection(users_ref, 1)

users_ref.stream

###############################
# Get

# Get a document
from google.cloud import firestore
import datetime
# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

me_ref = db.collection('users').document('amauvezin')
me_ref.set({
    'first': 'Arthur',
    'middle': 'Camille',
    'last': 'Mauvezin',
    'born': 1993,
    'age': datetime.datetime.now().year - 1993,
    'likes': [
        'rugby',
        'games'
    ]
})

doc_ref = db.collection(u'users').document(u'amauvezin')

try:
    doc = doc_ref.get()
    print(u'Document data: {}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'No such document!')

from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    last: str
    born: int
    likes: List[str]
    first: str
    age: int
    middle: str
    toto: Optional[str] = "default_str"

doc_ref = db.collection(u'users').document(u'amauvezin')
doc = doc_ref.get()
user = User(**doc.to_dict())
print(user)

# Get multiple documents
users_ref = db.collection('users')
users_ref.document('test1').set(user.dict())
users_ref.document('test1').update({'first': 'Test 1'})
users_ref.document('test1').update({'age': firestore.Increment(1)})
users_ref.document('test2').set(user.dict())
users_ref.document('test2').update({'first': 'Test 2'})
users_ref.document('test2').update({'age': firestore.Increment(2)})
users_ref.document('test3').set(user.dict())
users_ref.document('test3').update({'first': 'Test 3'})
users_ref.document('test3').update({'age': firestore.Increment(3)})

docs = db.collection(u'users').where('age', '==', 26).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# Get all doc from collection
docs = db.collection(u'users').stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))


# Query operators - <, <=, ==, >, >=, array_contains
docs = db.collection(u'users').where('age', '>', 27).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

docs = db.collection(u'users').where('likes', 'array_contains', 'rugby').stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

docs = db.collection(u'users').where('born', '==', 1993).where('age', '==', 28).stream()
#docs = db.collection(u'users').where('likes', 'array_contains', 'rugby').where('age', '>=', 28).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

museums = db.collection_group(u'landmarks').where(u'type', u'==', u'museum')
docs = museums.stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# Order by - order_by(z).order_by(x) - filter if value does not exist
docs = db.collection(u'users').order_by('age').limit(2).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# ASCENDING or DESCENDING
docs = db.collection(u'users').order_by('age', direction=firestore.Query.DESCENDING).limit(2).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

docs = db.collection(u'users').order_by('age', direction=firestore.Query.ASCENDING).stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()['age']))

# Start at
docs = db.collection(u'users').order_by('age', direction=firestore.Query.ASCENDING).start_at({'age': 27})
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()['age']))

# Paginate
users_ref = db.collection(u'users')
first_query = users_ref.order_by('age', direction=firestore.Query.ASCENDING).limit(2)

docs = first_query.stream()
alldocs = []

for doc in docs:
    alldocs.append(doc)
    print(u'{} => {}'.format(doc.id, doc.to_dict()['age']))

last_pop = alldocs[-1]
query = users_ref.order_by('age', direction=firestore.Query.ASCENDING).start_after(last_pop).limit(2)
docs = query.stream()

for doc in docs:
    alldocs.append(doc)
    print(u'{} => {}'.format(doc.id, doc.to_dict()['age']))

