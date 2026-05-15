import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re

INCLUDE_KEYWORDS = [
    "без ремонта", "требуется ремонт", "черновая отделка",
    "под отделку", "коробка дома", "без внутренней отделки"
]

EXCLUDE_KEYWORDS = [
    "евроремонт", "дизайнерский ремонт", "с ремонтом",
    "готов к проживанию", "заезжай и живи"
]


def is_no_repair(text):
    if not text:
        return False
    text_lower = text.lower()
    for exc in EXCLUDE_KEYWORDS:
        if exc in text_lower:
            return False
    for inc in INCLUDE_KEYWORDS:
        if inc in text_lower:
            return True
    return False


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        url = "https://www.avito.ru/moskovskaya_oblast?q=дом+коттедж+дача"
        await page.goto(url)
        await page.wait_for_timeout(3000)

        results = []

        for page_num in range(1, 4):
            print(f"Страница {page_num}...")

            try:
                await page.wait_for_selector("[data-marker='item']", timeout=10000)
                cards = await page.query_selector_all("[data-marker='item']")

                for card in cards:
                    try:
                        title_elem = await card.query_selector("[itemprop='name']")
                        title = await title_elem.inner_text() if title_elem else ""

                        price_elem = await card.query_selector("[itemprop='price']")
                        price = await price_elem.get_attribute("content") if price_elem else ""

                        link_elem = await card.query_selector("a")
                        link = await link_elem.get_attribute("href") if link_elem else ""
                        if link and not link.startswith("http"):
                            link = "https://www.avito.ru" + link

                        description = ""
                        address = ""

                        if link_elem:
                            async with page.context.expect_page() as new_page_info:
                                await link_elem.click()
                            detail_page = await new_page_info.value
                            await detail_page.wait_for_timeout(2000)

                            desc_elem = await detail_page.query_selector("[data-marker='item-view/item-description']")
                            description = await desc_elem.inner_text() if desc_elem else ""

                            address_elem = await detail_page.query_selector("[class*=address]")
                            address = await address_elem.inner_text() if address_elem else ""

                            await detail_page.close()

                        full_text = f"{title} {description}"
                        if is_no_repair(full_text):
                            results.append({
                                "title": title,
                                "price": price,
                                "url": link,
                                "description": description[:500],
                                "address": address,
                                "date": ""
                            })
                            print(f"✅ Найдено: {title[:50]}")

                    except Exception as e:
                        print(f"Ошибка карточки: {e}")
                        continue

                next_btn = await page.query_selector("[data-marker='pagination-button/next']")
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_timeout(3000)
                else:
                    break

            except Exception as e:
                print(f"Ошибка страницы: {e}")
                break

        await browser.close()

        df = pd.DataFrame(results)
        df.to_excel("avito_no_repair.xlsx", index=False)
        df.to_csv("avito_no_repair.csv", index=False, encoding="utf-8-sig")

        print(f"\n🎉 Готово! Найдено объявлений: {len(results)}")
        print("Файлы: avito_no_repair.xlsx и avito_no_repair.csv")


if __name__ == "__main__":
    asyncio.run(main())