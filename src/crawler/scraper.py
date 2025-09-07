import scrapy
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess

class IndiaCodeActsSpider(scrapy.Spider):
    name = "indiacode_acts"
    allowed_domains = ["sci.gov.in"]
    start_urls = ["https://www.sci.gov.in/"]  # obey robots!

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "AUTOTHROTTLE_ENABLED": True,
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }

    def parse(self, response):
        for href in response.css("a::attr(href)").getall():
            url = urljoin(response.url, href)
            if "showfile" in url or "/handle/" in url:
                yield scrapy.Request(url, callback=self.parse_law)
            elif self.should_follow(url):
                yield scrapy.Request(url, callback=self.parse)

    def parse_law(self, response):
        meta = {
            "source_url": response.url,
            "title": response.css("title::text").get(),
        }
        text = self.extract_text(response)  # html or delegate to pdf extractor
        yield {"text": text, "meta": meta}

    def should_follow(self, url): 
        return url.startswith("https://www.indiacode.nic.in/")

    def extract_text(self, r):
        return " ".join(r.css("body *::text").getall()).strip()


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "indiacode_acts.json": {"format": "json", "overwrite": True},
        }
    })
    process.crawl(IndiaCodeActsSpider)
    process.start()
