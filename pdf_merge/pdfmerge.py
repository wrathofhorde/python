from icecream import ic
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from merger import read_filenames, merge_pdfs

ic.disable()

def select_dir():
    tk.dirname = filedialog.askdirectory(
        initialdir="path",
        mustexist=True
    )

    ic(tk.dirname)

    text = tk.dirname if len(tk.dirname) else "Not selected"
    lbl_dir.configure(text=text)


def merge():
    tk.output = inp_file.get()

    if len(tk.output) < 5:
        messagebox.showerror("에러", "저장할 파일이름이 누락되었습니다.")
        return
    
    if len(tk.dirname) == 0:
        messagebox.showerror("에러", "파일 경로를 지정하지 않았습니다.")
    
    btn_merge.config(state="disabled")

    files = read_filenames(tk.dirname)
    files.sort()
    ic(files)
    merge_pdfs(tk.dirname, files, tk.output)

    btn_merge.config(state="normal")
    messagebox.showinfo("Success", "파일 병합이 완료되었습니다.")

tk = Tk()

tk.title("PDF Merger 1.1")

tk.geometry("480x120+400+400")
tk.resizable(False, False)

tk.dirname = ""
tk.output = "_merged.pdf"

lbl_dir = Label(tk, text="병합할 PDF 파일이 저장된 폴더를 선택하세요.", \
                 relief="solid", borderwidth=1)
lbl_dir.place(x=10, y=10, width=380, height=40)


btn_select = Button(tk, text="폴더 선택", command=select_dir)
btn_select.place(x=400, y=10, width=70, height=40)

lbl_file = Label(tk, text="병합될 파일명")
lbl_file.place(x=10, y=60, width=120, height=40)

inp_file = Entry(tk, width=10, borderwidth=2)
inp_file.place(x=140, y=60, width=250, height=40)
inp_file.insert(0, tk.output)

btn_merge = Button(tk, text="병  합", command=merge)
btn_merge.place(x=400, y=60, width=70, height=40)

tk.mainloop()