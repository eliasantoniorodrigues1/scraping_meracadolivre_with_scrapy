import scrapy


class MlSpider(scrapy.Spider):
    name = 'ml'
    # allowed_domains = ['mercadolivre.com']
    # //*[@id="root-app"]/div/section[2]/div/div[2]/div/ol/li[1]
    start_urls = ['https://www.mercadolivre.com.br/ofertas#nav-header']

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[@class="promotion-item default"]'):
            # xpath relativo com ponto no inicio
            price = i.xpath(
                './/span[@class="promotion-item__price"]//text()').getall()
            title = i.xpath(
                './/p[@class="promotion-item__title"]//text()').get()
            link = i.xpath('./a/@href').get()

            yield {
                "price": price,
                "tittle": title,
                "link": link
            }
        # pega a proxima pagina de forma dinamica
        next_page = response.xpath(
            '//a[contains(@title, "Próxima")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
