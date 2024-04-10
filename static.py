import pathlib


PATH_SUBCATEGORY_ZARA_FILE: pathlib.Path = (
    pathlib.Path.cwd() / "db" / "csv_subcat_zara.csv"
)
PATH_SUBCATEGORY_HM_FILE: pathlib.Path = (
    pathlib.Path.cwd() / "db" / "csv_subcat_hm.csv"
)
PATH_SUBCATEGORY_FASHIONNOVA_FILE: pathlib.Path = (
    pathlib.Path.cwd() / "db" / "csv_subcat_fashionnova.csv"
)
COLUMN_NAME_SUBCATEGORY_FILE: list = ["name", "url"]
