import scrapy


class StartechspiderSpider(scrapy.Spider):
    name = "startechspider"
    allowed_domains = ["www.startech.com.bd"]
    start_urls = ["https://www.startech.com.bd/"]

    def parse(self, response):
        product = response.xpath('//*[@id="product"]/div/div[1]/h1/text()').get()
        # Find the first table on the page
        table = response.xpath('//*[@id="specification"]/table').extract_first()

        if product is not None and table is not None:
            # yield {'product': product}
            data = {
                'product': product,
            }
            # Find all the rows in the table
            body = response.xpath('//*[@id="specification"]/table/tbody')
            length = len(body)
            print(f'SPIDER: found tbodys {length}')
            row_count = 0
            for content in body:
                rows = content.xpath('./tr')
                lr = len(rows)
                row_count += lr
                desc = {}
                for row in rows:
                    # Find all the columns in the row
                    columns = row.xpath('./td')

                    # Get the text from each column
                    column_texts = [col.xpath('.//text()').get() for col in columns]
                    [key, value] = column_texts
                    # desc.append(column_texts)

                    desc[key] = value
            data['description'] = desc
            yield data

        # Find all links on the page and follow them
        for href in response.xpath('//a/@href'):
            yield response.follow(href, self.parse)
