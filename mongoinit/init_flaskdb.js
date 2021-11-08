db.createUser({
    user: "flaskuser",
    pwd: "flaskpass",
    roles: [ { role: "readWrite", db: "flaskdb"} ]
});

db.createCollection("users");
users = [
    {
        "name": "Pista1",
        "pwd_hash": "hash1",
        "email": "pista1@x.y"
    },
    {
        "name": "Pista2",
        "pwd_hash": "hash2",
        "email": "pista2@x.y"
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

