import os
import tkinter
from tkinter import filedialog
import shutil
ventana = tkinter.Tk()
ventana.geometry("600x350")


def uploadFiles():
    curr_directory="./IMG"
    file_path = filedialog.askopenfilename(initialdir=curr_directory, title="Select Image", filetypes=[('Image Files', '*.PNG')])
    shutil.copy(file_path,curr_directory)
    print(file_path)
    names=file_path.split("/")
    names[len(names)-1]=names[len(names)-1].replace(".png","")
    print(names)
    file_old= curr_directory+"/"+names[len(names)-1]+".png"
    file_new= curr_directory+"/"+"toto"+".png"
    os.rename(file_old, file_new)


button_upload_img= tkinter.Button(ventana, text ="Upload", command = uploadFiles(),bg= "yellow").pack()

#cajaTexto = tkinter.Entry(ventana, font = "Helvetica 17")
#cajaTexto.pack()

#def name_img():
   #image_name = cajaTexto.get()
   #print(image_name)

#button_name_img= tkinter.Button(ventana, text ="Ingresa el nombre", command = name_img,bg= "skyblue")
#button_name_img.pack()

ventana.mainloop()