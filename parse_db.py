from genericpath import isfile
import os
from pathlib import Path
import fitz
import db_utils

source_dir = "data/papers"
out_dir = "data/images"


def process_doc(path, url):
    cnx = db_utils.init()
    doc = fitz.open(path)
    mkdirs(doc)
    paper_date = doc.metadata["creationDate"][2:6]
    paper_id = db_utils.get_paper_id_or_add(cnx, url, paper_date)

    process_pages(path, process_drawings, cnx, url, paper_id)
    process_pages(path, process_rasters, cnx, url, paper_id)


def process_pages(path, fun, cnx, url, date):
    doc = fitz.open(path)
    for i, page in enumerate(doc.pages()):
        try:
            fun(page, cnx, url, i+1, date)
        except Exception as e:
            print(f"Error {e} in {fun.__name__} on file: {path}")


def process_rasters(page, cnx, url, page_num, paper_id):
    images = page.get_images()
    doc_name = os.path.basename(page.parent.name)
    base_path = f"{out_dir}/{doc_name}/rasters/{page_num}"
    for index, image in enumerate(images):
        page.set_cropbox(page.get_image_rects(
            image[0])[0].intersect(page.mediabox))

        image_info = {
            "paper_id": paper_id,
            "page_num": page_num,
            "image_path": f"{base_path}-{index+1}.png",
            "page_text": page.get_text(),
            "img_text": None,
        }

        page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(
            image_info["image_path"])

        db_utils.insert_info_with_paper_id(cnx, **image_info)


def process_drawings(page, cnx, url, page_num, paper_id):
    drawings = page.get_drawings()
    bound = fitz.Rect()
    cont = True
    for d in drawings:
        for item in d["items"]:
            for p in item:
                if type(p) is fitz.Point:
                    bound.x0 = bound.x1 = p.x
                    bound.y0 = bound.y1 = p.y
                    cont = False
                    break
                if type(p) is fitz.Rect:
                    bound = p
                    cont = False
                    break
                if type(p) is fitz.Quad:
                    bound.x0 = bound.x1 = p.ul.x
                    bound.y0 = bound.y1 = p.ul.y
                    cont = False
                    break
            if not cont:
                break
        if not cont:
            break

    for d in drawings:
        for item in d["items"]:
            for p in item:
                if type(p) is fitz.Point:
                    bound.include_point(p)
                if type(p) is fitz.Rect:
                    bound.include_rect(p)
                if type(p) is fitz.Quad:
                    bound.include_point(p.ul)
                    bound.include_point(p.ur)
                    bound.include_point(p.ll)
                    bound.include_point(p.ur)

    if bound.is_empty:
        return None
    bound.intersect(page.mediabox)
    page.set_cropbox(bound)
    img = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc_name = os.path.basename(page.parent.name)
    base_path = f"{out_dir}/{doc_name}/drawings/{page_num}"
    img_txt = page.get_textbox(bound)

    image_info = {
        "paper_id": paper_id,
        "page_num": page_num,
        "image_path": f"{base_path}.png",
        "page_text": page.get_text(),
        "img_text": img_txt,
    }

    img.save(image_info["image_path"])

    db_utils.insert_info_with_paper_id(cnx, **image_info)


def mkdirs(doc):
    # doc = fitz.open(doc_path)
    doc_name = os.path.basename(doc.name)
    Path(f"{out_dir}/{doc_name}/drawings/").mkdir(exist_ok=True, parents=True)
    Path(f"{out_dir}/{doc_name}/rasters/").mkdir(exist_ok=True, parents=True)
