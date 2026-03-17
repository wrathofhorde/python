import os
import tkinter as tk
from tkinter import filedialog, messagebox
import win32com.client

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("오피스 파일 PDF 변환기")
        self.root.geometry("400x250")

        self.selected_path = tk.StringVar()

        # UI 요소 배치
        tk.Label(root, text="변환할 폴더를 선택하세요:", font=("Malgun Gothic", 10)).pack(pady=10)
        
        path_frame = tk.Frame(root)
        path_frame.pack(pady=5)
        
        tk.Entry(path_frame, textvariable=self.selected_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(path_frame, text="찾아보기", command=self.browse_folder).pack(side=tk.LEFT)

        self.status_label = tk.Label(root, text="대기 중...", fg="blue")
        self.status_label.pack(pady=20)

        tk.Button(root, text="PDF로 변환 시작", command=self.start_conversion, 
            bg="#4CAF50", fg="white", width=20, height=2).pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.selected_path.set(folder_selected)

    def word_to_pdf(self, word_app, file_path):
        out_path = os.path.splitext(file_path)[0] + ".pdf"
        doc = word_app.Documents.Open(os.path.abspath(file_path))
        doc.SaveAs(os.path.abspath(out_path), FileFormat=17) # 17: PDF format
        doc.Close()

    def ppt_to_pdf(self, ppt_app, file_path):
        out_path = os.path.splitext(file_path)[0] + ".pdf"
        presentation = ppt_app.Presentations.Open(os.path.abspath(file_path), WithWindow=False)
        presentation.SaveAs(os.path.abspath(out_path), 32) # 32: PDF format
        presentation.Close()

    def start_conversion(self):
        folder = self.selected_path.get()
        if not folder:
            messagebox.showwarning("경고", "먼저 폴더를 선택해주세요.")
            return

        files = [f for f in os.listdir(folder) if f.endswith(('.docx', '.pptx'))]
        if not files:
            messagebox.showinfo("알림", "변환할 워드나 파워포인트 파일이 없습니다.")
            return

        try:
            self.status_label.config(text="변환 중... 잠시만 기다려주세요.", fg="red")
            self.root.update()

            word_app = None
            ppt_app = None

            for file in files:
                full_path = os.path.join(folder, file)
                
                if file.endswith('.docx'):
                    if not word_app:
                        word_app = win32com.client.Dispatch("Word.Application")
                    self.word_to_pdf(word_app, full_path)
                
                elif file.endswith('.pptx'):
                    if not ppt_app:
                        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
                    self.ppt_to_pdf(ppt_app, full_path)

            if word_app: word_app.Quit()
            if ppt_app: ppt_app.Quit()

            self.status_label.config(text="변환 완료!", fg="green")
            messagebox.showinfo("성공", f"{len(files)}개의 파일이 PDF로 변환되었습니다.")
        
        except Exception as e:
            messagebox.showerror("오류", f"변환 중 오류 발생: {str(e)}")
            self.status_label.config(text="오류 발생", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()