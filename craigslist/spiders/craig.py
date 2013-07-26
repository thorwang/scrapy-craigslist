from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from craigslist.items import CraigslistItem

class CraigslistSpider(CrawlSpider):
    name = "craig"
    cities = ['boulder', 'denver', 'fortcollins', 'cosprings']
    allowed_domains = ['%s.craigslist.org' % city for city in cities]
    start_urls = ['http://%s.craigslist.org/web/' % city for city in cities]

    rules = (
            Rule(SgmlLinkExtractor(allow=("index\d00\.html", ), restrict_xpaths=('//p[@class="nextpage"]',)), follow=True),
            Rule(SgmlLinkExtractor(allow=("\d.html", ), restrict_xpaths=('//span[@class="pl"]',)), callback="parse_listing", follow=False),
        )

    def parse_listing(self, response):
        hxs = HtmlXPathSelector(response)

        item = CraigslistItem()
        item["title"] = ''.join(hxs.select("//h2[@class='postingtitle']/text()").extract()).strip()
        item["email"] = hxs.select("//section[@class='dateReplyBar']/a/text()").extract()
        item["date"] = hxs.select("//section[@class='dateReplyBar']/p[@class='postinginfo']/date/text()").extract()
        item["link"] = response.url

        return item
