# Scraper for quoka.de

## Install

```
$ git clone git@github.com:kuza/scrape-quoka.de.git .
$ cd scrape-quoka.de
$ virtualenv -p python2.7 --no-site-packages venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Start scraper

### Scrape by cities (demo db quokacities.sqlite)

```
$ scrapy crawl quokaspider
```

### Scrape all (demo db quokaall.sqlite)

```
$ scrapy crawl quokaallspider
```

### Scrape all with partners (demo db quokaallpartner.sqlite)

```
$ scrapy crawl quokaallpartnerspider
```
