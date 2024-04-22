import scrapy
from choclate_scraper.items import ChoclateProduct
class ChoclateSpider(scrapy.Spider):
    # Title of spider
    name = "choclate_spider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        # we loop through products and extract name,price,url
        products = response.css('product-item')

        product_item = ChocolateProduct()
        for product in products:
            product_item['name'] = product.css('a.product-item-meta__title::text').get(),
            product_item['price'] = product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
            product_item['url'] = product.css('div.product-item-meta a').attrib['href'],
            yield product_item
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk'+next_page
            yield response.follow(next_page_url,callback = self.parse)
