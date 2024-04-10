import csv
import logging
import pathlib

import static
from marketplaces import fashionnova, hm, zara


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("Parser Marketplaces")


def remove_csv(name_file: pathlib.Path) -> None:
    """Deleting a file

    Args:
        name_file (pathlib.Path): Path to the file to be deleted
    """
    if pathlib.Path.is_file(name_file):
        pathlib.Path.unlink(name_file)
        log.info(f"Remove file: {name_file}")


def create_or_update_csv(
    info_items_subcategory: list, name_file: pathlib.Path, column_names: list
) -> None:
    """Creating and Writing information to a file

    Args:
        info_items_subcategory (list): List of items and information on them
        name_file (pathlib.Path): Path to the file to be created
        column_names (list): list of keys for the dict
    """
    if not pathlib.Path.is_file(name_file):
        with open(name_file, mode="w", encoding="utf-8", newline="") as file:
            filewriter = csv.DictWriter(
                file, fieldnames=column_names, quotechar='"'
            )
            filewriter.writeheader()
    with open(name_file, mode="a", encoding="utf-8", newline="") as file:
        filewriter = csv.DictWriter(
            file, fieldnames=column_names, quotechar='"'
        )
        filewriter.writerows(info_items_subcategory)
    log.info(f"Create file: {name_file}")


def run():
    # Parser Zara
    parser_zara = zara.ParserZara()
    subcat_list_zara = parser_zara.get_subcategory()

    remove_csv(name_file=static.PATH_SUBCATEGORY_ZARA_FILE)
    create_or_update_csv(
        info_items_subcategory=subcat_list_zara,
        name_file=static.PATH_SUBCATEGORY_ZARA_FILE,
        column_names=static.COLUMN_NAME_SUBCATEGORY_FILE,
    )

    # Parser HM
    parser_hm = hm.ParserHm()
    subcat_list_hm = parser_hm.get_subcategory()

    remove_csv(name_file=static.PATH_SUBCATEGORY_HM_FILE)
    create_or_update_csv(
        info_items_subcategory=subcat_list_hm,
        name_file=static.PATH_SUBCATEGORY_HM_FILE,
        column_names=static.COLUMN_NAME_SUBCATEGORY_FILE,
    )

    # Parser FashionNova
    parser_fashionnova = fashionnova.ParserFashionNova()
    subcat_list_fashionnova = parser_fashionnova.get_subcategory()


if __name__ == "__main__":
    run()
