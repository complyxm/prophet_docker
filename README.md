## How to start Docker container
$ docker-compose build

$ docker-compose up -d

$ docker ps -a

$ docker exec -it コンテナ名orコンテナID /bin/bash

## Authentication in /app
export GOOGLE_APPLICATION_CREDENTIALS="[FILE_PATH]"