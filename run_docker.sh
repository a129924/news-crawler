docker build -t news_crawl_posgres . --no-cache
docker run --env-file ./env/db_config.env -d --name my_postgres_container -p 5432:5432 news_crawl_posgres