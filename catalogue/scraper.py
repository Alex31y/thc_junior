import asyncio
import logging
from . import database as db
from collections.abc import AsyncIterator
from playwright.async_api import async_playwright, Page
from sqlalchemy.orm import Session
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global progress counter
parts_scraped = 0

db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)
db.Base.metadata.create_all(bind=db.engine, checkfirst=True)


class ManufacturersJob:
    def __init__(self, target_href: str):
        self.target_href = target_href

    async def scrape_target(self, *, page: Page, session: Session) -> AsyncIterator:
        logging.info("Starting manufacturer scraping. This will take up to an hour...")
        await page.goto(self.target_href)
        base_href = await page.locator("head base").first.get_attribute("href") or ""
        manufacturers = await page.locator(".allmakes li a").all()
        logging.info(f"Found {len(manufacturers)} manufacturers")

        for i, manufacturer in enumerate(manufacturers, 1):
            name, href = (await manufacturer.text_content()).strip(), (await manufacturer.get_attribute("href")).strip()
            if name is not None and href is not None:
                manufacturer = db.insert_manufacturer(
                    session,
                    name=name,
                )
                logging.info(f"[{i}/{len(manufacturers)}] Processing manufacturer: {name}...")
                yield CategoriesJob(manufacturer.id, urljoin(base_href, href))


class CategoriesJob:
    def __init__(self, manufacturer_id: int, target_href: str):
        self.manufacturer_id = manufacturer_id
        self.target_href = target_href

    async def scrape_target(self, *, page: Page, session: Session) -> AsyncIterator:
        await page.goto(self.target_href)
        base_href = await page.locator("head base").first.get_attribute("href") or ""
        for category in await page.locator(".allcategories li a").all():
            name, href = (await category.text_content()).strip(), (await category.get_attribute("href")).strip()
            if name is not None and href is not None:
                category = db.insert_category(
                    session,
                    manufacturer_id=self.manufacturer_id,
                    name=name,
                )
                yield ModelsJob(category.id, urljoin(base_href, href))


class ModelsJob:
    def __init__(self, category_id: int, target_href: str):
        self.category_id = category_id
        self.target_href = target_href

    async def scrape_target(self, *, page: Page, session: Session) -> AsyncIterator:
        await page.goto(self.target_href)
        base_href = await page.locator("head base").first.get_attribute("href") or ""
        for model in await page.locator(".allmodels li a").all():
            name, href = (await model.text_content()).strip(), (await model.get_attribute("href")).strip()
            if name is not None and href is not None:
                model = db.insert_model(
                    session,
                    category_id=self.category_id,
                    name=name,
                )
                yield PartsJob(model.id, urljoin(base_href, href))


class PartsJob:
    def __init__(self, model_id: int, target_href: str):
        self.model_id = model_id
        self.target_href = target_href

    async def scrape_target(self, *, page: Page, session: Session) -> AsyncIterator:
        global parts_scraped
        await page.goto(self.target_href)
        for part in await page.locator(".allparts li a").all():
            if (name := await part.text_content()) is not None:
                elements = name.split("-")
                part_number = elements[0].strip()
                part_name = elements[1].strip()
                db.insert_part(
                    session,
                    model_id=self.model_id,
                    number=part_number.strip(),
                    name=part_name,
                )
                parts_scraped += 1
                if parts_scraped % 1000 == 0:
                    logging.info(f"Progress: {parts_scraped} parts scraped so far...")
        if False:
            yield  # TODO: Is there a better to way to force an "empty" AsyncIterator?!?


async def scraping_worker(*, scraper_queue: asyncio.Queue, page: Page, session: Session) -> None:
    while True:
        job = await scraper_queue.get()
        async for followup_job in job.scrape_target(page=page, session=session):
            await scraper_queue.put(followup_job)
        scraper_queue.task_done()


async def main():
    logging.info("Starting catalogue scraper...")
    scraper_queue: asyncio.Queue = asyncio.Queue()
    MANUFACTURERS_PAGE_HREF = "https://www.urparts.com/index.cfm/page/catalogue"
    await scraper_queue.put(ManufacturersJob(MANUFACTURERS_PAGE_HREF))

    async with async_playwright() as playwright:
        chromium = await playwright.chromium.launch(headless=True)

        for _ in range(1):  # Limiting to one to work well with Docker environment.
            asyncio.create_task(
                scraping_worker(
                    scraper_queue=scraper_queue,
                    page=await chromium.new_page(),
                    session=db.SessionLocal(),
                )
            )
        await scraper_queue.join()

        await chromium.close()

    logging.info(f"Scraping completed successfully! Total parts scraped: {parts_scraped}")


if __name__ == "__main__":
    asyncio.run(main())
