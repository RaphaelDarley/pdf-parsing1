from genericpath import isfile
import os
from pathlib import Path
import fitz

# print(doc.metadata)

source_dir = "scraped"
out_dir = "out"


def process_doc(name):
    doc = fitz.open(f"{source_dir}/{name}")
    doc_name = os.path.basename(doc.name)
    Path(f"{out_dir}/{doc_name}/").mkdir(exist_ok=True, parents=True)
    for page in doc.pages():
        process_page(page)


def process_page(page):
    # process_drawings(page)
    process_images(page)


def process_images(page):
    images = page.get_images()
    ocr_text = page.get_ocr_text()
    for image in images:


def process_drawings(page):
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
    dir_path = f"{out_dir}/{doc_name}/"

    img.save(f"{dir_path}{page.number}.png")
    img_txt = page.get_textbox(bound)
    with open(f"{dir_path}{page.number}.img.txt", "w", encoding="utf-8") as f:
        f.write(img_txt)
    with open(f"{dir_path}{page.number}.page.txt", "w", encoding="utf-8") as f:
        f.write(page.get_text())


if __name__ == '__main__':
    files = [f for f in os.listdir(source_dir) if isfile(f"{source_dir}\{f}")]

    # name = "JHL-test1.pdf"
    for num, name in enumerate(files):
        process_doc(name)
        print(f"finished {num +1}/{len(files)}: {name}")
        break

    # for page_num in range(1, 27, 1):
    #     process_page(doc, page_num)


# print(page.get_image_info())
# print(page.get_svg_image())
# print(page.get_text())
# print(page.get_textbox())
