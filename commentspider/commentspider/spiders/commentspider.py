# coding=utf-8
__author__ = "yubol@splunk.com"

import time
from scrapy.spiders import Spider
from items import CommentspiderItem, MovieInfoItem
import csv
from scrapy import Request


class MovieInfoSpider(Spider):
    name = 'movie_info_extractor'
    start_urls = []

    with open('items.csv', 'r') as f:
        csv_rdr = csv.reader(f)
        next(csv_rdr)
        for row in csv_rdr:
            start_urls.append(row[-1])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    to_delete = "\r\n\t "
    translate_table = dict((ord(char), None) for char in to_delete)

    def parse(self, response):
        item = MovieInfoItem()

        item['movie_name'] = response.xpath('.//*[@id="content"]/h1/span[1]/text()').extract()
        item['director'] = response.xpath('.//a[@rel="v:directedBy"]/text()').extract()
        item['actor_list'] = ' '.join([ _ for _ in response.xpath('.//a[@rel="v:starring"]/text()').extract()])
        item['description'] = response.xpath('.//span[@property="v:summary"]/text()').\
            extract()[0].translate(self.translate_table).replace('<br>', '')
        item['duration'] = response.xpath('.//span[@property="v:runtime"]/text()').extract()
        item['category'] = ' '.join([ _ for _ in response.xpath('.//span[@property="v:genre"]/text()').extract()])
        item['date'] = response.xpath('//span[@class="year"]/text()').extract()[0].replace('(', '').replace(')', '')
        time.sleep(2)
        yield item


class CommentSpider(Spider):
    name = 'comment_extractor'
    start_urls = []

    with open('items.csv', 'r' ) as f:
        csv_rdr = csv.reader(f)
        next(csv_rdr)
        for row in csv_rdr:
            start_urls.append(row[-1] + 'comments?sort=new_score&status=P')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    to_delete = "*#$¥%\r\n\t'\"(),.!?，。！？ "
    translate_table = dict((ord(char), None) for char in to_delete)

    def parse(self, response):
        item = CommentspiderItem()
        movie_name = response.xpath('//*[@id="content"]/h1/text()').extract()#.replace(u" 短评")
        comments = response.xpath('//*[@class="comment"]')
        for comment in comments:
            item['movie_name'] = movie_name
            # item['movie_comment_title'] = comment.xpath('.//h2/a/text()').extract()[0]
            item['movie_comment_content'] = comment.xpath('.//p/text()').extract()[0].translate(self.translate_table)
            yield item

        time.sleep(2)
        next_url = response.xpath('//*[@id="paginator"]/a[@class="next"]/@href').extract()
        if next_url:
            next_url = response.url.split('?')[0] + '' + next_url[0]
            print '..........>>', next_url
            yield Request(next_url, headers=self.headers)

