from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def pdfminer_config(line_overlap, word_margin, char_margin,line_margin, detect_vertical):
    laparams = LAParams(line_overlap=line_overlap,
                        word_margin=word_margin,
                        char_margin=char_margin,
                        line_margin=line_margin,
                        detect_vertical=detect_vertical)
    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    return (interpreter, device)

def find_textboxes(layout_obj):
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes(child))
        return boxes
    return []

def write_text(text_file, text):
    text_file.write(text + "\n")

text_file = open('output.txt', 'w')
with open("./file.pdf", 'rb') as f:
    interpreter, device = pdfminer_config(line_overlap=0.5, word_margin=0.1, char_margin=2, line_margin=0.5, detect_vertical=True)
    for page in PDFPage.get_pages(f):
        interpreter.process_page(page)  # ページを処理する。
        layout = device.get_result()  # LTPageオブジェクトを取得。
        boxes = find_textboxes(layout)
        for box in boxes:
            # write_text(text_file, box.get_text().strip())
            print(box.get_text().strip() + "\n")

text_file.close()
