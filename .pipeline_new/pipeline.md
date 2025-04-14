

```bash
docker-compose up
```

[apache airflow docker hub](https://hub.docker.com/r/apache/airflow/tags)

alternate
```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```

```bash
docker compose down --volumes --remove-orphans
docker compose up --build
```

```bash
sudo lsof -i :8080
```

```bash
docker ps  # to see running containers
docker stop <container_id_or_name>  # replace with the relevant container ID or name
```

remove all containers
```bash
docker rm -f $(docker ps -aq)
```

restart webserver
```bash
docker-compose restart airflow-webserver
```
Restart the webserver and scheduler if using Docker:
```bash
docker-compose restart airflow-webserver airflow-scheduler
```



list images
```bash
docker images
```
delete an image
```bash
docker rmi <image_id_or_name>
```

list all images
```bash
docker images -a
```

remove all docker images
```bash
docker rmi $(docker images -q)
```

save docker compose up logs to dockerlogs file in project directory
```bash
docker-compose up > dockerlogs.txt 2>&1
```

save docker compose up logs to dockerlogs file in project directory (running in detached mode)
```bash
docker-compose up -d
docker-compose logs -f > dockerlogs.txt 2>&1
```