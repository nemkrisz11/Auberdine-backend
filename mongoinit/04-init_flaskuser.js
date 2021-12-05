db.createUser({
    user: "flaskuser",
    pwd: "flaskpass",
    roles: [ { role: "readWrite", db: "flaskdb"} ]
});
