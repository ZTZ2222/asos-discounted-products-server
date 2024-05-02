import asyncio
import random
from datetime import datetime, timezone
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from src.services.product import (
    delete_old_products,
    insert_product,
    select_one,
    update_product,
)
from src.schemas.product import SProduct
from src.telegram import send_product_tg

load_dotenv()

brand_list = [
    {
        "name": "newBalance_footwear",
        "url": "15892?attribute_10992=61388&",
    },
    {
        "name": "levis_jeans_jeans",
        "url": "7083?attribute_10992=61377&attribute_1047=8393&",
    },
    {
        "name": "levis_sweats",
        "url": "7083?attribute_10992=61382&",
    },
    {
        "name": "theNorthFace_outerwear",
        "url": "19899?attribute_10992=61380&",
    },
    {
        "name": "converse_footwear_trainers",
        "url": "2611?attribute_10992=61388&attribute_1047=8606&",
    },
    {
        "name": "newEra_accessories_cap",
        "url": "17372?attribute_1047=8275&",
    },
    {
        "name": "hugo",
        "url": "27909?",
    },
    {
        "name": "birkenstock",
        "url": "7421?",
    },
    {
        "name": "ugg_footwear_boots",
        "url": "2609?attribute_10992=61388&attribute_1047=8585&",
    },
    {
        "name": "vans_footwear_trainers",
        "url": "14751?attribute_10992=61388&attribute_1047=8606&",
    },
    {
        "name": "drMartens",
        "url": "4650?attribute_10992=61388&",
    },
]

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Cookie": "browseCountry=TR; browseCurrency=GBP;",
}


async def get_data(session: aiohttp.ClientSession, brand: Dict, offset: int) -> None:
    url = f"https://www.asos.com/api/product/search/v2/categories/{brand.get('url')}offset={offset}&limit=199&range=sale&store=ROE&lang=en-GB&currency=GBP&rowlength=4&channel=desktop-web&country=TR&keyStoreDataversion=h7g0xmn-38"

    message_counter = 0

    async with session.get(url=url, headers=headers) as response:
        data: Dict[str, Any] = await response.json()
        products: List[Dict] = data.get("products", [])
        if products:
            for product in products:
                current_price = product.get("price").get("current").get("value")

                previous_price = product.get("price").get("previous").get("value")
                if not previous_price:
                    previous_price = product.get("price").get("rrp").get("value")

                try:
                    discount_percent = round((1 - current_price / previous_price) * 100)
                except:
                    discount_percent = 0

                product_data = SProduct(
                    id=product.get("id"),
                    name=product.get("name"),
                    brand_name=product.get("brandName"),
                    current_price=product.get("price").get("current").get("value"),
                    previous_price=previous_price,
                    discount_percent=discount_percent,
                    currency=product.get("price").get("currency"),
                    url=product.get("url"),
                    images=[product.get("imageUrl")]
                    + product.get("additionalImageUrls"),
                    product_code=product.get("productCode"),
                    selling_fast=product.get("isSellingFast"),
                    updated_at=datetime.now(timezone.utc),
                )

                existing_product = await select_one(id=product_data.id)
                if not existing_product:
                    product_db = await insert_product(product_data)
                elif (
                    existing_product
                    and existing_product.currency != product_data.currency
                ):
                    product_db = await update_product(product_data)
                else:
                    product_db = None

                if product_db and product_db.discount_percent >= 20:
                    await send_product_tg(product_db)
                    message_counter += 1

                    if message_counter % 10 == 0:
                        sleep_duration = random.uniform(2, 4)
                        await asyncio.sleep(sleep_duration)


async def gather_data():
    async with aiohttp.ClientSession() as session:
        for brand in brand_list:
            url = f"https://www.asos.com/api/product/search/v2/categories/{brand.get('url')}offset=0&limit=199&range=sale&store=ROE&lang=en-GB&currency=GBP&rowlength=4&channel=desktop-web&country=TR&keyStoreDataversion=h7g0xmn-38"
            response = await session.get(url=url, headers=headers)
            if response.status == 200:
                data = await response.json()
                total_items = data.get("itemCount")
            else:
                print(response.status)
                return

            tasks = []
            for offset in range(0, total_items, 199):
                task = asyncio.create_task(
                    get_data(session=session, brand=brand, offset=offset)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)
            sleep_duration = random.uniform(2, 4)
            await asyncio.sleep(sleep_duration)

        session.close()

    # Delete old products
    await delete_old_products()


# def job():
#     asyncio.create_task(gather_data())


# # Schedule the job to run
# schedule.every().day.at(os.getenv("SCHEDULE_TIME"),
#                         timezone('Asia/Bishkek')).do(job)


async def main():
    # while True:
    #     schedule.run_pending()
    #     await asyncio.sleep(1)
    await gather_data()


if __name__ == "__main__":
    asyncio.run(main())
