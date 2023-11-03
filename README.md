# sreality.cz scraper

```
Use scrapy framework to scrape the first 500 items (title, image url) from sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker compose command so that I can just run "docker-compose up" in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.
```

# Prerequisities:
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose v2](https://docs.docker.com/compose/install/)

# Start
```bash
$ git clone git@github.com:mountDoom2/task-sreality-scraper.git
$ cd task-sreality-scraper
$ docker-compose up
```