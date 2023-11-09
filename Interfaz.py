import os
import tkinter
from tkinter import filedialog
import shutil
import main
import cv2 as cv
import luma
import brightness
import nidity
from PIL import ImageTk, Image
window = tkinter.Tk()
window.geometry("920x650")

File_Final_Name="placeholder"
close_button=0

def uploadFiles():
    if (os.path.exists("./IMG/23.PNG")):
        os.remove("./IMG/23.PNG")
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
    ilusion(file_new)

def ilusion(file_new):
    correct_orientation, correct_centered, total_difference=main.main(file_new)
    print("AJSDKASJDNMASKDJNASMDJ")
    image = Image.open(file_new)
    img= image.resize((240,320))
    photo = ImageTk.PhotoImage(img)
    if correct_orientation==True:
        checked_orientation="Yes"
    else:
        checked_orientation="No"

    if correct_centered==True:
        checked_centered="Yes"
    else:
        checked_centered="No"
    # Label widget to display the image
    color_image = cv.imread(file_new, cv.IMREAD_COLOR)
    square_data = luma.get_square_data(file_new)
    point_to_get_brightness, center = brightness.nearest_point_center(square_data[1], square_data[3])
    red,green,blue=brightness.get_brightness(color_image, point_to_get_brightness)
    total_brigthness= (0.2126*red)+(0.7152*green)+(0.0722*blue)
    print(total_brigthness)
    if(total_brigthness>=170 and total_brigthness<=250):
        check_brightness="Yes"
    else:
        check_brightness="No"
    sharpness_value=nidity.calculate_nidity(file_new)
    print(sharpness_value)
    if(sharpness_value>=0.15):
        sharpness_checked="Yes"
    else:
        sharpness_checked="No"
    
    total_difference=int(total_difference)

    label = tkinter.Label(window, image=photo,width=240, height=320)
    label.pack()
    label_orientation = tkinter.Label(window, text = f'Does it pass the orientation test? {checked_orientation}, by {correct_orientation}', font="Helvetica 12")
    label_orientation.pack()
    label_brightness = tkinter.Label(window, text = f'Does it pass the brightness test? {check_brightness}, by red: {red}, green: {green}, blue: {blue}', font="Helvetica 12")
    label_brightness.pack()
    label_centered = tkinter.Label(window, text = f'Does it pass the centerness test? {correct_centered}, by {total_difference} pixels', font="Helvetica 12")
    label_centered.pack()
    label_sharpness = tkinter.Label(window, text = f'Does it pass the sharpness test? {sharpness_checked}, by {sharpness_value}', font="Helvetica 12")
    label_sharpness.pack()
    window.mainloop()


def close():
   #win.destroy()
   window.quit()
   close_button=1

tkinter.Button(window, text= "Close the Window", font=("Calibri",14,"bold"), command=close).pack(pady=20)
button_upload_img = tkinter.Button(window, text ="Upload", command = uploadFiles,bg= "yellow", font="Helvetica 17").pack()
    
window.mainloop()