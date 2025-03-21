<a id="readme-top"></a>
# learn Airflow 
ensure no docker containers running:
```bash
sudo docker container ls
```
remove all dangling images:
```bash
sudo docker image prune
```

build airflow project
```bash
sudo docker-compose up --build
```
open [airflow UI @localhost:8080](http://localhost:8080) \<replace port in case change in docker-compose.yml file>

to stop execution CTRL + C and run:
1. to stop the containers without removing them:
    ```bash
    sudo docker-compose stop
    ```
2. to stop and remove containers, networks, and volumes:
    ```bash
    sudo docker-compose down
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>