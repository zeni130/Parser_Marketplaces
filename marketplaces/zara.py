from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs


class ParserZara:
    SKIP_SUBCATEGORIES = [
        "view all",
        "special prices",
        "new",
        "stores",
        "gift card",
        "gift cardcheck balanceactivate card",
        "gift receipt",
        "press",
        "about",
        "collection",
    ]

    def __init__(self):
        pass

    def get_subcategory(self) -> list:
        res = []

        with sync_playwright() as pw:
            browser = pw.webkit.launch()
            page = browser.new_page()
            page.goto("https://www.zara.com/us/")
            soup = bs(page.content(), features="html.parser")

            for cat in soup.findAll(
                "ul",
                class_="layout-categories-category__subcategory "
                "layout-categories-category__subcategory--hidden",
            ):
                for subcat in cat:
                    text_subcat = subcat.text
                    link = subcat.find("a").get("href")
                    if link is not None:
                        if text_subcat.lower() in self.SKIP_SUBCATEGORIES:
                            continue
                        subcat = {"name": text_subcat, "url": link}
                        res.append(subcat)

        return res
