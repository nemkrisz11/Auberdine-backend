db.createCollection("users");
users = [
    {
        "name": "Pista1",
        "pwd_hash": "hash1",
        "email": "pista1@x.y",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Pista2",
        "pwd_hash": "hash2",
        "email": "pista2@x.y",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Dr. Goldschmidt Balázs",
        "pwd_hash": "hash3",
        "email": "goldschmidt@iit.bme.hu",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "John von Neumann",
        "pwd_hash": "hash4",
        "email": "neumann@x.z",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Isaac Newton",
        "pwd_hash": "hash5",
        "email": "newton@gravity.org",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Vladimir Putin",
        "pwd_hash": "hash6",
        "email": "vlad@kreml.ru",
        "friends": [],
        "friend_requests": []
    }
];
db.users.insertMany(users);

db.createCollection("places");

places = [
    {
        "name": "Kurva jó étterem",
        "address": "Bivalybasznád, fő utca 3."
    }
]

db.places.insertMany(places);

