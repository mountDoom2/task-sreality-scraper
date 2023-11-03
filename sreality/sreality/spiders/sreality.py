import logging
from typing import Iterable

import scrapy

from sreality.items import SRealityItem

logger = logging.getLogger(__name__)


class SReality(scrapy.Spider):
    """Scrapy spider for parsing SReality estate ads (flats for sale).

    There are few limitations in this implementation:
        * number of ads is not configurable (strictly set to 500),
        * only applicable for flats for sale (no housing or renting scraping is supported),
        * no pagination support (not a problem as for this use case, maximum page size for API is
            as of now 999).
    """

    name = "sreality"

    def start_requests(self) -> Iterable[scrapy.Request]:
        """Make an API call to sreality API.

        Using API is the simplest solution to achieve the goal. Another way how to achieve the goal
        is to scrape the rendered data from request. However SReality uses dynamic loading using JavaScript
        and Scrapy alone is not strong enough to parse such content. We would have to use JavaScript
        rendering service like Splash or Selenium for which there exist Scrapy plugins.
        """
        url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500"
        yield scrapy.Request(url, callback=self.process_api_response)

    def process_api_response(
        self, response: scrapy.http.Response
    ) -> Iterable[SRealityItem]:
        """Get relevant data (title, image URL) from API response.

        Data are obtained in a safe manner in case of potential API change.
        JSON objects that do not contain necessary data are omitted and logged.

        :return: Iterable of parsed items.
        """
        # root -> _embedded -> estates -> name
        #                              -> _links -> images[0] -> href
        estates_json = response.json().get("_embedded", {}).get("estates", [])
        for estate in estates_json:
            name = estate.get("name")
            url = next(iter(estate.get("_links", {}).get("images", []))).get("href")

            if not name or not url:
                logger.warning(
                    "Estate ad does not contain requested data, omitting from processing."
                )
                logger.debug("Omitted object: %s", estate)
                continue

            yield SRealityItem(title=name, image_url=url)
