#The needed libraries are imported
import os
import tkinter
from tkinter import filedialog
import shutil
import orientation
import cv2 as cv
import luma
import brightness
import nidity
from PIL import ImageTk, Image

#The window screen for the app is created
window = tkinter.Tk()
window.geometry("920x650")

#Useful global variables are declared
File_Final_Name="placeholder" #Variable that will contain the path to the image uploaded
close_button=0 #Variable that checks whether the close button has been pressed

#--------------------------------------------------Functions--------------------------------------------------------
#Function that copies the image to the desired directory and renames it as desired
def uploadFiles():
    if (os.path.exists("./IMG/1.PNG")): #Checks if the file that contains the image is already created from a previous iteration
        os.remove("./IMG/1.PNG") #If it is, it deletes it 
    curr_directory="./IMG" #Checks the directory where the images will be stored
    file_path = filedialog.askopenfilename(initialdir=curr_directory, title="Select Image", filetypes=[('Image Files', '*.PNG')]) #Opens
    #the file directory while filtering files to only PNG to simplify the uploading process
    shutil.copy(file_path,curr_directory) #Creates a copy of the image selected by the user into the determined directory
    
    #Process for obtaining the image actual name
    names=file_path.split("/") #Separates the image original path using the /
    names[len(names)-1]=names[len(names)-1].replace(".PNG","") #Removes the .PNG from the file
    names[len(names)-1]=names[len(names)-1].replace(".PNG","") #Removes the .PNG from the file
    file_old= curr_directory+"/"+names[len(names)-1]+".PNG" #creates a path with the new location of the image with the old name
    file_new= curr_directory+"/"+"1"+".PNG" #Creates a path with the new location of the image with the name 1.PNG
    os.rename(file_old, file_new) #Renames the image to the name 1.PNG
    ilusion(file_new) #Passes the new path of the image to the function ilusion
 
#The function that obtains all the data from the other programs
def ilusion(file_new): 
    correct_orientation, correct_centered, total_difference=orientation.main(file_new) #Pases the path of the image to the function
    #main imported from the file orientation.py that checks the orientation and the centered values 
    image = Image.open(file_new) #Opens the image for it to be shown on the tkinter app
    img= image.resize((240,320)) #Resizes the image to show a better resolution
    photo = ImageTk.PhotoImage(img) #Converts the photo into tkinter useful data
    if correct_orientation==True: #Checks if the orientation passed by the function main from orientation.py is True, so that it is 
        #Correctly oriented
        checked_orientation="Yes" #Variable that tells whether the orientation is good or not
    else:
        checked_orientation="No" #Variable that tells whether the orientation is good or not

    if correct_centered==True: #Checks if the centered value passed by the function main from orientation.py is valid or not.
        checked_centered="Yes"#Variable that tells whether the centered is good or not
    else:
        checked_centered="No" #Variable that tells whether the centered is good or not
    # Label widget to display the image
    color_image = cv.imread(file_new, cv.IMREAD_COLOR)

    #Functions from brightness.py that are explained in the original file
    square_data = luma.get_square_data(file_new)
    point_to_get_brightness, center = brightness.nearest_point_center(square_data[1], square_data[3])
    red,green,blue=brightness.get_brightness(color_image, point_to_get_brightness) #Gets the brightness in red, green and blue light
    total_brigthness= (0.2126*red)+(0.7152*green)+(0.0722*blue) #Calculates the total brightness in a scale 0 to 255
    if(total_brigthness>=170 and total_brigthness<=250): #Checks if the total brightness is between 170 and 250, so that it is correct
        check_brightness="Yes" #Variable that tells whether the brightness is good or not
    else:
        check_brightness="No" #Variable that tells whether the brightness is good or not
    sharpness_value=nidity.calculate_nidity(file_new) #Gets the sharpness of the image as it passes the path of the image to the
    #function that calculates sharpness in the file nidity.py
    if(sharpness_value>=0.15): #Checks if the sharpness is the minimu accepted
        sharpness_checked="Yes" #Variable that tells whether the sharpness is good or not
    else:
        sharpness_checked="No" #Variable that tells whether the sharpness is good or not
    
    total_difference=int(total_difference) #Round the difference from the center pixels as decimal pixels do not exist

    #The sintaxis for showing something on the app goes as following:
    #label_declaration.pack() = tkinter.label(screen_to_be_show,things_to_be_shown,//the following are optional: width:pixels,height:pixels,font:style size)
    #label_declaration_name.pack()
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

    #The main loop that, in this case, refreshes the content of the page
    window.mainloop()

#Function that closes the window when the button is pressed
def close():
   #win.destroy()
   window.destroy()
   close_button=1

#Buttons:
tkinter.Button(window, text= "Close the Window", font=("Calibri",14,"bold"), command=close).pack(pady=20)
button_upload_img = tkinter.Button(window, text ="Upload", command = uploadFiles,bg= "yellow", font="Helvetica 17").pack()
    
#Main loop that initializates the screen and keeps it running
window.mainloop()