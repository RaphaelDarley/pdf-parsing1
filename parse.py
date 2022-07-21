from genericpath import isfile
import os
from pathlib import Path
import fitz

# print(doc.metadata)

source_dir = "scraped"
out_dir = "out"


def process_doc(name):
    process_pages(name, process_drawings)
    process_pages(name, process_rasters)


def process_pages(name, fun):
    doc = fitz.open(f"{source_dir}/{name}")
    doc_name = os.path.basename(doc.name)
    Path(f"{out_dir}/{doc_name}/drawings/").mkdir(exist_ok=True, parents=True)
    Path(f"{out_dir}/{doc_name}/rasters/").mkdir(exist_ok=True, parents=True)
    for page in doc.pages():
        try:
            fun(page)
        except Exception as e:
            print(f"Error {e} in {fun.__name__} on file: {name}")


# def process_page(page):
#     # process_drawings(page)
#     process_rasters(page)


def process_rasters(page):
    images = page.get_images()
    doc_name = os.path.basename(page.parent.name)
    base_path = f"{out_dir}/{doc_name}/rasters/{page.number}"
    for index, image in enumerate(images):
        # print(page.get_image_rects(image[0]))
        page.set_cropbox(page.get_image_rects(
            image[0])[0].intersect(page.mediabox))
        save_info(f"{base_path}-{index+1}",
                  page.get_pixmap(matrix=fitz.Matrix(2, 2)), page.get_text())


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
    base_path = f"{out_dir}/{doc_name}/drawings/{page.number}"
    img_txt = page.get_textbox(bound)
    save_info(base_path, img, page.get_text(), img_txt=img_txt)


def save_info(base_path, img, page_txt, img_txt=False):
    img.save(f"{base_path}.png")
    if not img_txt == False:
        with open(f"{base_path}.img.txt", "w", encoding="utf-8") as f:
            f.write(img_txt)
    with open(f"{base_path}.page.txt", "w", encoding="utf-8") as f:
        f.write(page_txt)


if __name__ == '__main__':
    files = [f for f in os.listdir(source_dir) if isfile(f"{source_dir}\{f}")]

    # name = "JHL-test1.pdf"
    for num, name in enumerate(files):
        process_doc(name)
        print(f"finished {num +1}/{len(files)}: {name}")

        doc = fitz.open(f"{source_dir}/{name}")
        print(name)
        print(doc.metadata)

        break

    # for page_num in range(1, 27, 1):
    #     process_page(doc, page_num)


# print(page.get_image_info())
# print(page.get_svg_image())
# print(page.get_text())
# print(page.get_textbox())
