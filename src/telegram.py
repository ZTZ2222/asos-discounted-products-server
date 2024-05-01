import os
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils import formatting as fm

from .models.models import ProductOrm

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.MARKDOWN_V2)
user_id = os.getenv("USER_ID")


async def send_product_tg(product: ProductOrm):
    base_url = "https://www.asos.com/"
    if product.selling_fast:
        named_url = fm.TextLink(product.name + " (⚡️)", url=base_url + product.url)
    else:
        named_url = fm.TextLink(product.name, url=base_url + product.url)

    if product.discount_percent < 40:
        price_with_discount = (
            f"🏷 £{product.current_price} ( - {product.discount_percent}% )"
        )
    else:
        price_with_discount = fm.Bold(
            f"🔥 £{product.current_price} ( - {product.discount_percent}% )"
        )

    content = fm.as_list(
        fm.Pre(f"***{product.brand_name}***"),
        fm.as_key_value("Модель", named_url),
        fm.as_key_value("Текущая цена", price_with_discount),
        fm.as_key_value("Прежняя цена", f"£{product.previous_price}"),
        fm.as_key_value("Артикул", product.product_code),
        fm.HashTag("_".join(str(product.brand_name).lower().split(" "))),
    )

    await bot.send_photo(
        chat_id=user_id, photo=product.images[0], caption=content.as_markdown()
    )
