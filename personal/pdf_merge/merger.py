import os

from icecream import ic
from PyPDF2 import PdfMerger, PdfReader

ic.disable()

def read_filenames(path):
    filelist = os.listdir(path)
    ic(filelist)
    filenames = [file for file in filelist if file.endswith(".pdf") or file.endswith(".PDF")] 
    
    if not filenames:
        return []
    else:
        return filenames


def merge_pdfs(path, files, merged_file="_merged.pdf"):
    merger = PdfMerger()
    
    for file in files:
        if merged_file not in file:
            merger.append(PdfReader(open(path + "/" + file, "rb")))
            # merger.append(PdfReader(open(file, "rb")))

    merger.write(path + '/' + merged_file)

    ic("PDF 병합 완료")


if __name__ == "__main__":
    path = "C:/Users/wrath/Documents/한글디렉토리"
    # path = "C:/Users/wrath/Documents/[한글]디렉토리"
    files = read_filenames(path)
    print(files)
    merge_pdfs(path, files)

