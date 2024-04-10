import json

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import dataclasses


@dataclasses.dataclass
class ParserFashionNova:
    URL = "https://www.fashionnova.com"
    URLS = {
        "women": "https://www.fashionnova.com",
        "man": "https://www.fashionnova.com/pages/men",
    }

    def get_subcategory(self):
        res = {}

        with sync_playwright() as pw:
            browser = pw.webkit.launch(headless=True)
            page = browser.new_page()

            for gender, url in self.URLS.items():
                page.goto(url=url, timeout=60000)
                soup = bs(page.content(), features="html.parser")

                header_content_prerender = soup.find(
                    "div", class_="header-content-prerender"
                )
                scripts = header_content_prerender.find_all("script")

                for script in scripts:
                    vl = script.get("data-sub-cat-lvl")
                    if not vl:
                        continue

                    match vl:
                        case "1":
                            brand_name = script.get("data-brand-name")
                            cat_handle = script.get("data-sub-cat-handle")
                            res[brand_name] = res.get(brand_name) or {}
                            res[brand_name][cat_handle] = {}
                        case "2":
                            brand_name = script.get("data-brand-name")
                            cat_handle = script.get("data-sub-cat-handle")
                            res_title = script.get("data-sub-cat-title")
                            res[brand_name][cat_handle][res_title] = []
                        case "3":
                            brand_name = script.get("data-brand-name")
                            cat_handle = script.get("data-sub-cat-handle")
                            res_title = script.get("data-sub-cat-title")
                            res_cat = {
                                "subcat": script.get("data-info-title"),
                                "url": self.URL + script.get("data-info-url"),
                            }

                            list_ = res[brand_name][cat_handle][res_title]
                            if list_:
                                list_.append(res_cat)
                                res[brand_name][cat_handle][res_title] = list_
                            else:
                                res[brand_name][cat_handle][res_title] = [
                                    res_cat
                                ]

        with open("db/fashion_nova.json", "w") as outfile:
            json.dump(res, outfile)
