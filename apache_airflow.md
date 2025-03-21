<a id="readme-top"></a>
# Apache Airflow

## Docker Airflow

[documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

check is docker version meets minimum requirements
```bash
sudo docker run --rm "debian:bookworm-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```

fetch [docker-compose for airflow](https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml)
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'
```

example prerequisite:
- docker
- docker-compose

<p align="right">(<a href="#readme-top">back to top</a>)</p>