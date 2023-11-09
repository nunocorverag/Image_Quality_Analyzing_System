import os
import tkinter
from tkinter import filedialog
import shutil
ventana = tkinter.Tk()
ventana.geometry("600x350")

def open_file():
    curr_directory = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=curr_directory, title="Select Image", filetypes=[('Image Files', '*.jpg')])
    print(file_path)
    return (file_path)
    '''
    archivo = filedialog.askopenfilename(title="abrir", initialdir = "C:/")
    normal_image = list(archivo)
    reversed_image = list(reversed(normal_image))
    list_name_image = []
    if ((reversed_image[0]) == "g") and ((reversed_image[1]) == "n"):
         for i in reversed_image:
            if i != "/":
                   list_name_image.append(i)
            else:
                break
    name_image = "".join(list(reversed(list_name_image)))
    return name_image'''

def uploadFiles():
    curr_directory="./IMG"
    file_name="test"
    file_path = filedialog.askopenfilename(initialdir=curr_directory, title="Select Image", filetypes=[('Image Files', '*.jpg')])
    shutil.copy(file_path,curr_directory)
    

def open_image():
    img = open_file() #Whatever the given image is
    save_path = "/IMG"
    file_name = "test"
    complete_name = os.path.join(save_path, file_name)
    uploadFiles()
    print(img) 

button_upload_img= tkinter.Button(ventana, text ="Upload", command = uploadFiles(),bg= "yellow").pack()

#cajaTexto = tkinter.Entry(ventana, font = "Helvetica 17")
#cajaTexto.pack()

#def name_img():
   #image_name = cajaTexto.get()
   #print(image_name)

#button_name_img= tkinter.Button(ventana, text ="Ingresa el nombre", command = name_img,bg= "skyblue")
#button_name_img.pack()

ventana.mainloop()