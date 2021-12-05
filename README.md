# Auberdine-backend

[API docs](./docs/api.md), [DB docs](./docs/db.md)

## Build and run
```
docker-compose build 
docker-compose up
```

Configure which dump is to be loaded. If you want to load a db dump, then copy it to the `mongoinit`
folder as `db_dump`, and set the following variable in `docker-compose.yml`:
```
LOAD_MONGODB_DUMP: "true"
```
If the variable is not set, a default testdb is loaded.

Shutting down with deleting data volumes too:

```
docker-compose down -v
```

## Run tests
First start the backend, then:
```
docker exec -t flask /var/www/test/run_tests.sh
```

Run tests and show stdout (prints) too:
```
docker exec -t flask /var/www/test/run_tests.sh --stdout
```

## Misc
Dump mongodb in mongo container:
```
mongodump -o /data/db/db_dump -d flaskdb mongodb://flaskuser:flaskpass@localhost:27017
```

Restore mongodb in mongo container
```
mongorestore mongodb://flaskuser:flaskpass@localhost:27017/flaskdb /docker-entrypoint-initdb.d/db_dump/flaskdb
```

Don't read this:
```
db.places.aggregate([ {$match: {"pictures.0": {$exists: true}}}, {$project: {imageSize: {$binarySize: {$arrayElemAt: ["$pictures", 0]}}}}, {$sort: {"imageSize": 1}}])
```
