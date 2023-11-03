# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from sreality.utils import close_db, connect_db_from_env


class SRealityPipeline:
    """Pipeline for processing SReality estate ads.

    While processing estate ad, it is stored into database.
    Since there always will be only one spider needed for this case,
    db connection and operations are handled directly in this class.
    For more complex solutions, it would be reasonable to have a layer
    responsible for db operations, error handling etc. which would be
    might be injected into and used by spiders that need to persist the data.
    """

    def __init__(self) -> None:
        """Constructor."""
        self.conn = None
        self.cursor = None

    def close_spider(self, _: scrapy.Spider) -> None:
        """Once all items are processed, close the database connection."""

        close_db(self.conn, self.cursor)
        self.conn = self.cursor = None

    def open_spider(self, _: scrapy.Spider) -> None:
        """Open database connection and create table for ads."""
        self.conn, self.cursor = connect_db_from_env()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS ads (
            title VARCHAR(64),
            image_url VARCHAR(128)
            );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def process_item(self, item: scrapy.Item, _: scrapy.Spider) -> scrapy.Item:
        """Process item after initial loading from Spider. Just store to database."""
        query = "INSERT INTO ads VALUES (%s, %s);"
        self.cursor.execute(query, (item["title"], item["image_url"]))
        self.conn.commit()
        return item
