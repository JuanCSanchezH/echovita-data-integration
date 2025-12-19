import scrapy

from obituaries.items import ObituariesItem


class ObituariesSpider(scrapy.Spider):
    name = "obituaries"
    allowed_domains = ["www.echovita.com"]
    start_urls = ["https://www.echovita.com/us/obituaries"]

    def parse(self, response):
        """
        Parse the listing page to find all obituary cards and extract their links.
        """
        min_slash_count = 4
        cards = response.xpath(
            "//div[contains(@class, 'col-12') and contains(@class, 'col-lg-6') and contains(@class, 'h-100')]"
        )

        self.logger.info(f"Found {len(cards)} obituary cards on page")

        seen_links = set()
        for card in cards:
            # Find each card
            link = card.xpath(".//a[contains(@href, '/us/obituaries/')]/@href").get()

            if link and link.count("/") >= min_slash_count and link not in seen_links:
                seen_links.add(link)
                yield response.follow(link, self.parse_obituary)

    def parse_obituary(self, response):
        """
        Parse the obituary detail page to extract:
        - Full name
        - Birth date and death date
        - Obituary text
        """
        item = ObituariesItem()

        item["full_name"] = self._extract_full_name(response)
        item["date_of_birth"], item["date_of_death"] = self._extract_dates(response)
        item["obituary_text"] = self._extract_obituary_text(response)

        yield item

    def _extract_full_name(self, response):
        """Extract the full name from the page."""
        full_name = response.xpath(
            "//p[contains(@class,'my-auto') and contains(@class,'h1') "
            "and contains(@class,'text-white') and contains(@class,'font-weight-bolder')]/text()"
        ).get()
        return full_name.strip() if full_name else None

    def _extract_dates(self, response):
        """
        Extract birthdate and death date from the date paragraph.
        Returns: (birth_date, death_date)
        """
        # Find the paragraph containing the dates
        date_paragraph = response.xpath(
            "//p[contains(@class,'mt-2') and contains(@class,'mb-1') and contains(@class,'text-white') "
            "and contains(@class,'font-weight-bold')]"
        )

        if not date_paragraph:
            return None, None

        # Parse dates from format: "December 24, 1933 - December 15, 2025 (91 years old)"
        date_text = date_paragraph.xpath(".//text()").getall()
        date_line = " ".join([text.strip() for text in date_text])

        # If there is no "-", probably it's a death date
        if " - " not in date_line:
            return None, date_line.strip()

        parts = date_line.split(" - ", 1)
        birth_date = parts[0].strip() if parts[0] else None

        # Extract death date and remove the age part "(91 years old)"
        death_date_part = parts[1].strip() if len(parts) > 1 else ""
        death_date = death_date_part.split("(")[0].strip() if "(" in death_date_part else death_date_part

        return birth_date, death_date

    def _extract_obituary_text(self, response):
        """Extract the obituary text from the page."""
        paragraphs = response.xpath("//div[@id='obituary']//p//text()").getall()

        if not paragraphs:
            return None

        obituary_text = " ".join([text.strip() for text in paragraphs if text.strip()])
        return obituary_text if obituary_text else None
