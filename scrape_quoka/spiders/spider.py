# -*- coding: utf-8 -*-

import scrapy
import re

from datetime import datetime


TAG_RE = re.compile(r'<[^>]+>')


def clean_str(text):
    return ' '.join(TAG_RE.sub('', text).split())


def date_to_int(dt_time):
    return 10000*dt_time.year + 1000*dt_time.month + dt_time.day


def str_to_int(value):
    if value:
        return int(value)
    return 0


class QuokaSpider(scrapy.Spider):
    name = 'quokaspider'
    start_urls = ['http://www.quoka.de/immobilien/bueros-gewerbeflaechen/']

    def parse(self, response):
        for url in response.xpath(
                '//div/strong[contains(text(), "Ort")]/ancestor::*[1]'
                '/div[@class="cnt"]//li/a[contains(@href, ".html")]/@href').re(
                    '.*cat_.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_city)

    def parse_city(self, response):
        try:
            pages = int(
                response.selector.xpath(
                    '//div[contains(@class, "page-navigation-bottom")]'
                    '//strong[contains(text(), "Seite 1")]/ancestor::*[1]'
                    '/strong/text()').re_first('^\d+$'))
        except (TypeError, ValueError):
            yield None

        for i in range(1, pages+1):
            url = (
                '/kleinanzeigen/' +
                response.url.split('/')[-1][:-5] +
                '_page_{}.html'.format(i))
            yield scrapy.Request(response.urljoin(url), self.parse_page)

    def parse_page(self, response):
        formdata = dict()
        for form_input in response.xpath(
                '//form[@class="SearchFormInsert"]/input').extract():
            sel = scrapy.Selector(text=form_input)

            name = sel.xpath('//@name').extract_first()
            value = sel.xpath('//@value').extract_first()

            formdata.update({name: value})

        formdata.update(classtype="of")

        yield scrapy.FormRequest(
            url=response.url,
            formdata=formdata,
            callback=self.parse_line)

    def parse_line(self, response):
        for url in response.xpath(
                '//div[@id="ResultListData"]//li[contains(@class, "hlisting")]'
                '/div[contains(@class, "image")]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_obj)

    def parse_obj(self, response):
        now = datetime.utcnow()
        data = dict(
            Boersen_ID=21,
            OBID=0,  # parse
            erzeugt_am=date_to_int(now),  # crape date
            Anbieter_ID=None,  # Immobilienscout24 for partner
            Anbieter_ObjektID=None,
            Immobilientyp=u"Büros, Gewerbeflächen",
            Immobilientyp_detail=None,
            Vermarktungstyp=u"kaufen",
            Land=u"Deutschland",
            Bundesland=None,
            Bezirk=None,
            Stadt='',  # parse
            PLZ='',  # parse
            Strasse=None,
            Hausnummer=None,
            Uberschrift='',  # parse
            Beschreibung='',  # parse
            Etage=None,
            Kaufpreis=0,  # parse
            Kaltmiete=None,
            Warmmiete=None,
            Nebenkosten=None,
            Zimmeranzahl=None,
            Wohnflaeche=None,
            Monat=now.month,  # curent month
            url=response.url,  # detail url
            Telefon=0,  # parse
            Erstellungsdatum=0,  # parse
            Gewerblich=0)  # parse

        obid = response.xpath(
            '//div[@class="date-and-clicks"]/strong/text()').re_first('\d+')
        stadt = response.xpath(
            '//span[@class="address location"]//span[@class="locality"]'
            '/text()').extract_first()
        plz = response.xpath(
            '//span[@class="address location"]'
            '//span[@class="postal-code"]/text()').re_first('\d+')
        uberschrift = response.xpath(
            '//h1[@itemprop="name"]/text()').extract_first()
        beschreibung = response.xpath(
            '//div[@itemprop="description"]/text()').extract_first()
        kaufpreis = response.xpath(
            '//div[contains(@class,"price")]/strong/'
            'span/text()').extract_first()
        if kaufpreis:
            kaufpreis = ''.join(re.findall('(\d+)[,.]', kaufpreis))

        telefon_url = response.xpath(
            '//a[contains(@onclick,"displayphonenumber.php")]'
            '/@onclick').extract_first()
        if telefon_url:
            m = re.search('load\( \'(.+?)\'', telefon_url)
            if m:
                url = m.group(1)
                request = scrapy.Request(
                    response.urljoin(url), self.parse_phone)
                request.meta['item'] = data

        erstellungsdatum = response.xpath(
            '//div[contains(text(), "Datum:")]'
            '/following-sibling::*').extract_first()
        if 'Heute' in erstellungsdatum:
            erstellungsdatum = date_to_int(now)
        elif 'Gestern' in erstellungsdatum:
            erstellungsdatum = date_to_int(now.replace(day=now.day-1))
        else:
            erstellungsdatum = ''.join(re.findall('\d+', erstellungsdatum))

        gewerblich = bool(response.xpath(
            '//div[@class="cust-type"]/text()').re_first('Gewerblicher'))

        data.update(
            OBID=str_to_int(obid),
            Stadt=stadt,
            PLZ=plz,
            Uberschrift=uberschrift,
            Beschreibung=clean_str(beschreibung),
            Kaufpreis=str_to_int(kaufpreis),
            Erstellungsdatum=str_to_int(erstellungsdatum),
            Gewerblich=int(gewerblich))

        yield data

    def parse_phone(self, response):
        item = response.meta['item']

        telefon = response.xpath('//span/text()').extract_first()
        telefon = ''.join(re.findall('\d+', telefon))

        item['Telefon'] = str_to_int(telefon)

        return item
