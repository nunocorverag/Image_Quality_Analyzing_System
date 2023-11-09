import os
import tkinter
from tkinter import filedialog
import shutil
import main
ventana = tkinter.Tk()
ventana.geometry("600x350")


def uploadFiles():
    curr_directory="./IMG"
    file_path = filedialog.askopenfilename(initialdir=curr_directory, title="Select Image", filetypes=[('Image Files', '*.PNG')])
    shutil.copy(file_path,curr_directory)
    print(file_path)
    names=file_path.split("/")
    names[len(names)-1]=names[len(names)-1].replace(".PNG","")
    names[len(names)-1]=names[len(names)-1].replace(".PNG","")
    print(names)
    file_old= curr_directory+"/"+names[len(names)-1]+".PNG"
    file_new= curr_directory+"/"+"23"+".PNG"
    os.rename(file_old, file_new)
    main.main(file_new)


button_upload_img= tkinter.Button(ventana, text ="Upload", command = uploadFiles(),bg= "yellow").pack()

ventana.mainloop()