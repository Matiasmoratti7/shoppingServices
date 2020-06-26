# How to

Standing in /shoppingServices/"service_name", build the image of each service:

```
docker image build -t "service_name" -f docker/Dockerfile .
```

Pull mongo image using:

```
docker pull mongo
```

Then, standing on /shoppingServices, run the containers with docker-compose:

```
docker-compose -f docker/docker-compose.yml up
```

This will start the services on the following ports:
```
shopping_cart_rs ---> 5000
storage_rs ---> 4000
user_auth_rs ---> 3000
email_rs ---> 2000
```

Both storage_rs and user_auth_rs will have its own DB in a separate container built from "mongo" image.

## Persistence

Since there's no way in Windows to persist Mongo data when binding a container to a specific folder in the file system,
all the data from storage_rs and user_auth_rs are stored in two different volumes managed by Docker (storage_db and user_db)