

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