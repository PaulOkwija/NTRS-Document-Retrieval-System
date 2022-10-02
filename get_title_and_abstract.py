"""Get title and abstract from pdf"""
import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from flashtext import KeywordProcessor

KEY_PRO = KeywordProcessor(case_sensitive=False)

def list_to_string(listvalue):
    """list to string function"""
    my_string = ' '.join(listvalue)
    return my_string


def get_text(pdf_file):
    """ get pdf data of first page"""
    try:
        file_path = open(pdf_file, 'rb')
        pdf_parser = PDFParser(file_path)
        pdf_document = PDFDocument(pdf_parser)
        if not pdf_document.is_extractable:
            raise PDFTextExtractionNotAllowed
        pdf_rsrcmgr = PDFResourceManager()
        pdf_laparams = LAParams()
        pdf_device = PDFPageAggregator(pdf_rsrcmgr, laparams=pdf_laparams)
        pdf_interpreter = PDFPageInterpreter(pdf_rsrcmgr, pdf_device)
        pdf_textdata = []
        for page in PDFPage.create_pages(pdf_document):
            pdf_interpreter.process_page(page)
            pdf_layout = pdf_device.get_result()
            for obj in pdf_layout._objs:
                if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                    pdf_textdata.append(obj.get_text().replace('\n', '_'))
            break
        return pdf_textdata
    except Exception as error:
        return error



def get_abstract(textdata):
    """get abs related content"""
    data = []
    doi_num = []
    words = ['A B S T R A C T    _', 'a b s t r a c t_', 'abstract', 'abstract:', 'Abstract:']
    KEY_PRO.add_keywords_from_list(words)
    for sent in textdata:
        found_sent = []
        found_sent = KEY_PRO.extract_keywords(sent)
        if len(found_sent) > 0:
            if len(sent) > 20:
                doi_num = sent
    if len(doi_num) == 0:
        doi_num = max(textdata, key=len)
        for i in textdata:
            if "*" not in i:
                data.append(i)
        doi_num = max(data, key=len)
    return doi_num.replace("_", "")


def journal_abs(text_data):
    """get abstract from pdf"""
    pdf_abs = get_abstract(text_data)
    # print('pdf_abs: ', pdf_abs)
    if "KEYWORDS:" in pdf_abs:
        abstract_lst = pdf_abs.split("KEYWORDS:")
        abs_content = abstract_lst[0]
        pdf_abs = abs_content.replace('ABSTRACT:', '')
    
    pdf_abs = pdf_abs.replace('Abstract', '')
    pdf_abs = pdf_abs.replace('ABSTRACT:', '')
    
    return pdf_abs