#!/bin/sh

set -e

# Scrape sreality.cz and store results to db
cd sreality
scrapy crawl sreality

# Start webserver
flask run