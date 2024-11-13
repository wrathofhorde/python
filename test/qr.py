import qrcode
import tkinter

qr_info = "https://www.youtube.com/watch?v=YbbnOmYmyhs&t=5s"
qr_filename = "qr_img.png"

qr = qrcode.make(qr_info)
qr.save(qr_filename)

wind = tkinter.Tk()
wind.title("QR CODE")
qr_image = tkinter.PhotoImage(file=qr_filename)
qr_label = tkinter.Label(wind, image=qr_image)
qr_label.pack()

wind.mainloop()
