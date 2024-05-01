import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("C:\\Users\\91765\\PycharmProjects\\toyota contest\\serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendencerealtime-6838c-default-rtdb.firebaseio.com/"
})

ref=db.reference('students')


data={
    "14": {
        'name':"Prem Kumar",
        'major':'cybersecurity',
        'starting_year':2022,
        'total_attendence':90,
        'standing':'g',
        'year':2,
        'last_attendence_time':'2024-3-11 00:54:34'

    },

    "15": {
        'name': "Ramaguru Radhakrishnan",
        'major': 'cybersecurity',
        'starting_year': 2017,
        'total_attendence': 93,
        'standing': 'g',
        'year': 5,
        'last_attendence_time': '2024-1-10 12:54:34'

    },

    "16": {
        'name': "Navarang CD",
        'major': 'cybersecurity',
        'starting_year': 2022,
        'total_attendence': 94,
        'standing': 'g',
        'year': 2,
        'last_attendence_time': '2024-1-4 10:04:24'

    },
    "25": {
        'name': "B Rushi Reddy",
        'major': 'cybersecurity',
        'starting_year': 2022,
        'total_attendence': 50,
        'standing': 'g',
        'year': 2,
        'last_attendence_time': '2024-7-06 14:34:34'

    },
    "76": {
        'name': "Sree Chandan",
        'major': 'cybersecurity',
        'starting_year': 2022,
        'total_attendence': 97,
        'standing': 'g',
        'year': 2,
        'last_attendence_time': '2024-1-4 10:04:24'

    },
    "39": {
        'name': "Sai Tejas",
        'major': 'cybersecurity',
        'starting_year': 2022,
        'total_attendence': 100,
        'standing': 'b',
        'year': 1,
        'last_attendence_time': '2024-1-3 06:04:24'

    },
    "6": {
        'name': "B Krishna Veni",
        'major': 'cybersecurity',
        'starting_year': 2022,
        'total_attendence': 100,
        'standing': 'b',
        'year': 1,
        'last_attendence_time': '2024-1-3 06:04:24'

    }





}

for key,value in data.items():
    ref.child(key).set(value)