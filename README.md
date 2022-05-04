## Get started

Docker & Docker Compose are required.

First, lets prepare your environment:

```sh
cp sample.env .env
```

Then, execute the project

```sh
docker-compose up --build --detach
```

Finally follow the logs via:

```sh
docker-compose logs --follow api
```

The server will be running at `localhost:8080`, all the changes in there will be reflected immediately.
