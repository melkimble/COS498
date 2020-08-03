'''
https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
https://github.com/pdfminer/pdfminer.six
'''

import io
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def pdfs2Array(testDataFolder):
    # empty array that will contain all parsed pdf files for testing.
    parsed_pdfs = []
    fname=[]
    for pdf in os.listdir(testDataFolder):
        if pdf.endswith(".pdf"):
            try:
                ThePDFFile = (os.path.join(testDataFolder, pdf))
                # pdf file converted to text
                test = convert_pdf_to_txt(ThePDFFile)
                # list of parsed pdf files
                parsed_pdfs.append(test)
                # list of pdf filenames
                fname.append(ThePDFFile)
            except Exception:
                # if pdf cannot be read, continue to the next pdf
                continue
    return(parsed_pdfs,fname)

'''
text = convert_pdf_to_txt("D:/Dropbox/01_School/18SP/COS498/FinalProject/TestingData/Adam and Michelle Campbell, Pulpit Harbor Salt Pond, N. Haven.pdf")
#print(text)
'''