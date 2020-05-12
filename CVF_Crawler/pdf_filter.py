
import os
import traceback
from pdfminer.pdfpage import PDFPage

def filter_repeat(main_dir):
    conf_dir = os.path.join(main_dir,'conference')
    work_dir = os.path.join(main_dir,'workshop')
    conf_files = [i for i in os.listdir(conf_dir) if i[-4:] =='.pdf']
    work_files = [i for i in os.listdir(work_dir) if i[-4:] =='.pdf']
    repeat_files = set(conf_files) & set(work_files)
    for i in repeat_files:
        os.remove(os.path.join(work_dir,i))
    return repeat_files

def filter_lack(work_dir):
    work_files = [i for i in os.listdir(work_dir) if i[-4:] =='.pdf']
    for fname in work_files:
        try:
            with open(os.path.join(work_dir,fname), 'rb') as infile:
                page_num = len(list(PDFPage.get_pages(infile)))
            if page_num < 7:
                os.remove(os.path.join(work_dir,fname))
        except:
            print(fname)
            continue

if __name__=='__main__':
    filter_repeat('dataset/train')
    filter_lack('dataset/train/workshop')
    filter_repeat('dataset/test')
    filter_lack('dataset/test/workshop')