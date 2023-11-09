import tkinter
from tkinter import filedialog
ventana = tkinter.Tk()
ventana.geometry("600x350")

def abrirArchivo():
    archivo = filedialog.askopenfilename(title="abrir", initialdir = "C:/")
    print(archivo)

button_upload_img= tkinter.Button(ventana, text ="Translada la imágen hacia la capeta IMG, ubicada dentro de Image_Quality_Analyzing_System", command = abrirArchivo,bg= "yellow").pack()

cajaTexto = tkinter.Entry(ventana, font = "Helvetica 17")
cajaTexto.pack()

image_name = cajaTexto.get()
print(image_name)

button_name_img= tkinter.Button(ventana, text ="Ingresa el nombre", command = "name_img",bg= "skyblue")
button_name_img.pack()

ventana.mainloop()