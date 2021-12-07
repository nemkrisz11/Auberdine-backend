#!/bin/bash

if [ "$LOAD_MONGODB_DUMP" = "true" ]; then
  MONGO_URI="mongodb://$MONGODB_USERNAME:$MONGODB_PASSWORD@localhost/$MONGO_INITDB_DATABASE"
  mongo "$MONGO_URI" --eval "db.places.remove({})"
  mongo "$MONGO_URI" --eval "db.reviews.remove({})"
  mongo "$MONGO_URI" --eval "db.users.remove({})"
  mongorestore $MONGO_URI /docker-entrypoint-initdb.d/db_dump/flaskdb
fi
