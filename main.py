from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject
import os


def page_merger(page1, page2, left_to_right):
    total_width = page1.mediaBox.upperRight[0] + page2.mediaBox.upperRight[0]
    total_height = max([page1.mediaBox.upperRight[1], page2.mediaBox.upperRight[1]])
    new_page = PageObject.createBlankPage(None, total_width, total_height)
    if left_to_right:
        new_page.mergePage(page1)
        new_page.mergeTranslatedPage(page2, page1.mediaBox.upperRight[0], 0)
    else:
        new_page.mergePage(page2)
        new_page.mergeTranslatedPage(page1, page1.mediaBox.upperRight[0], 0)
    return new_page


def half_page(input_pdf, page_num, left_to_right):
    page = input_pdf.getPage(page_num)
    total_width = page.mediaBox.upperRight[0] * 2
    total_height = page.mediaBox.upperRight[1]
    new_page = PageObject.createBlankPage(None, total_width, total_height)
    if not left_to_right:
        new_page.mergePage(page)
    else:
        new_page.mergeTranslatedPage(page, page.mediaBox.upperRight[0], 0)
    return new_page


def make_booklet(pdf_path, left_to_right):
    input_pdf = PdfFileReader(open(pdf_path, "rb"), strict=False)
    output = PdfFileWriter()
    output.addPage(half_page(input_pdf, 0, left_to_right))
    page_num = 1
    if (input_pdf.numPages - 1) % 2 != 0:
        output.addPage(half_page(input_pdf, 1, not left_to_right))
        page_num += 1
    for i in range(page_num, int(input_pdf.numPages / 2)):
        page1 = input_pdf.getPage(i)
        page2 = input_pdf.getPage(input_pdf.numPages - (i - page_num) - 1)
        if left_to_right:
            output.addPage(page_merger(page1, page2, i % 2 == 0))
        else:
            output.addPage(page_merger(page2, page1, i % 2 != 0))
    file_path = os.path.dirname(os.path.abspath(pdf_path))
    output.write(open(file_path + "\\result.pdf", "wb"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = input("Enter file path:")
    left_to_right = bool(int(input("Is it left to right? (0 for false, 1 for true)")))
    make_booklet(path, left_to_right)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
