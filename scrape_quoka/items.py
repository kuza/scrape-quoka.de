# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeQuokaItem(scrapy.Item):
    Boersen_ID = scrapy.Field()
    OBID = scrapy.Field()  # parse
    erzeugt_am = scrapy.Field()  # crape date
    Anbieter_ID = scrapy.Field()  # Immobilienscout24 for partner
    Anbieter_ObjektID = scrapy.Field()
    Immobilientyp = scrapy.Field()
    Immobilientyp_detail = scrapy.Field()
    Vermarktungstyp = scrapy.Field()
    Land = scrapy.Field()
    Bundesland = scrapy.Field()
    Bezirk = scrapy.Field()
    Stadt = scrapy.Field()  # parse
    PLZ = scrapy.Field()  # parse
    Strasse = scrapy.Field()
    Hausnummer = scrapy.Field()
    Uberschrift = scrapy.Field()  # parse
    Beschreibung = scrapy.Field()  # parse
    Etage = scrapy.Field()
    Kaufpreis = scrapy.Field()  # parse
    Kaltmiete = scrapy.Field()
    Warmmiete = scrapy.Field()
    Nebenkosten = scrapy.Field()
    Zimmeranzahl = scrapy.Field()
    Wohnflaeche = scrapy.Field()
    Monat = scrapy.Field()  # curent month
    url = scrapy.Field()  # detail url
    Telefon = scrapy.Field()  # parse
    Erstellungsdatum = scrapy.Field()  # parse
    Gewerblich = scrapy.Field()
