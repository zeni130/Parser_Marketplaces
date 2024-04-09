import json

from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright


class ParserHm:
    def __init__(self):
        pass

    @staticmethod
    def get_subcategory():
        urls = [
            "https://www2.hm.com/en_us/women/products/view-all.html",
            "https://www2.hm.com/en_us/men/products/view-all.html"
        ]

        res = []
        with sync_playwright() as pw:
            browser = pw.webkit.launch(headless=False)
            page = browser.new_page()

            for url in urls:
                page.goto(url=url)
                soup = bs(page.content(), features="html.parser")

                page_sidebar = soup.find("aside", class_="page-sidebar")
                script = page_sidebar.find("script")
                props = (
                    str(script.contents[0])
                    .split(" = ")[1]
                    .rsplit("\n", maxsplit=1)[0]
                )
                data = json.loads(props)
                data_cats = []
                for data_title in data["menuList"]:
                    if data_title["categoryTitle"] != "Shop by Product":
                        continue
                    data_cats = data_title["links"]

                for category in data_cats:
                    if category["text"] == "View All":
                        continue
                    link_cat = "https://www2.hm.com" + category["url"]
                    page.goto(link_cat)
                    soup_cat = bs(page.content(), features="html.parser")

                    page_sidebar_cat = soup_cat.find(
                        "aside", class_="page-sidebar"
                    )
                    script_cat = page_sidebar_cat.find("script")
                    props_cat = (
                        str(script_cat.contents[0])
                        .split(" = ")[1]
                        .rsplit("\n", maxsplit=1)[0]
                    )
                    data_cat = json.loads(props_cat)
                    data_subcat = []
                    for title_cat in data_cat["menuList"]:
                        if title_cat["categoryTitle"] != "Shop by Product":
                            continue
                        data_subcat = title_cat["links"]

                    for subcat in data_subcat:
                        if subcat["text"] == "View All" or subcat in data_cats:
                            continue

                        if not subcat["children"]:
                            subcat_data = {
                                "name": subcat["text"],
                                "url": subcat["url"]
                            }
                            res.append(subcat_data)
                            continue

                        for children in subcat["children"]:
                            subcat_data = {
                                "name": children["text"],
                                "url": children["url"]
                            }
                            res.append(subcat_data)

            return res
