# Auberdine-backend

## Build and run the backend
```
docker-compose build 
docker-compose up
```

## Modifying source files
No restart is needed, as `--reload` in `entrypoint.sh` makes the server update.

## Shutdown backend
```
docker-compose down
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

## Manual testing

```
curl localhost:80/PATH
```


