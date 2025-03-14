import glob

from PyPDF2 import PdfMerger, PdfReader

def read_filenames(path):
    filenames = glob.glob(path + "/*.pdf")

    if not filenames:
        return []
    else:
        return filenames


def merge_pdfs(path, files, merged_file="merged_file.pdf"):
    merger = PdfMerger()
    
    for file in files:
        if merged_file not in file:
            merger.append(PdfReader(open(file, "rb")))

    merger.write(path + '/' + merged_file)

    # print("PDF 병합 완료")


if __name__ == "__main__":
    path = "./temp"
    files = read_filenames(path)
    print(files)
    merge_pdfs(path, files)

