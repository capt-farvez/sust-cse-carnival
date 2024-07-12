import scrapy

class StartechSpider(scrapy.Spider):
    name = 'startech'
    start_urls = ['https://www.startech.com.bd/']  # Replace with your starting URL

    def parse(self, response):
        # Find the first table on the page
        table = response.xpath('//*[@id="specification"]/table').extract_first()

        if table is not None:
            # Find all the rows in the table
            rows = response.xpath('//*[@id="specification"]/table/tr')

            for row in rows:
                # Find all the columns in the row
                columns = row.xpath('./td')

                # Get the text from each column
                column_texts = [col.xpath('.//text()').get() for col in columns]

                # Yield the columns' text
                yield {'data': column_texts}

        # Find all links on the page and follow them
        for href in response.xpath('//a/@href'):
            yield response.follow(href, self.parse)
