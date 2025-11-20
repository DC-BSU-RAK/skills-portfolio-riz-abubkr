from tkinter import *   # Import all Tkinter module
from PIL import ImageTk, Image # import pil module(for images)
import random  # Import random to select a random joke



#Loading and Preparing Joke Data From the File
def load_jokes():
    jokes = []# Empty list to store jokes 
    with open("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt", "r") as file_handler: # Opening the text file 
        lines = file_handler.readlines()   # Read all lines from file into a list
        for line in lines:# create loop for every line in the file
            line = line.strip() #Delete extra space
            if "?" in line: # Adiing "?" in each line so it will look like a joke
                parts = line.split("?", 1) # Split the sentence into two parts
                setup = parts[0] + "?" # first part is question and a "?"is added
                punchline = parts[1]# Second part is punchline
                           
            jokes.append((setup, punchline))# Store joke as a tuple 

    return jokes                           



# Load jokes once at start of program
jokes_list = load_jokes() # Call function to load jokes from file
current_joke = None # Variable to store currently selected joke



# FUNCTION TO SHOW RANDOM JOKE 
def tell_joke():
    global current_joke
    current_joke = random.choice(jokes_list) # Picks a  random joke from list
    setup_label.config(text=current_joke[0])# Display the joke on screen
    punchline_label.config(text="") # Clears old punchline 


#FUNCTION TO SHOW PUNCHLINE
def show_punchline():
    if current_joke: # Only show punchline if a joke was selected
        punchline_label.config(text=current_joke[1]) # Display the punchline below joke


#FUNCTION TO LOAD A NEW RANDOM JOKE
def next_joke():
 tell_joke()             



#MAIN TKINTER WINDOW SETUP
root = Tk() #Create the main window 
root.title("Joke Assistant") #title of the window
root.geometry("500x300") # Set the window size
root.config(bg="#FFFFFF") # Set background color of window
root.resizable(False, False)  # Output Window size is fixed


#ADD BACKGROUND IMAGE
bg_img = Image.open("Assessment 1 - Skills Portfolio/A1 - Resources/BG image,png.jpeg")
bg_img = bg_img.resize((500, 300)) # resize to window size
bg_image = ImageTk.PhotoImage(bg_img)
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)



# LABEL TO DISPLAY JOKE SETUP 
setup_label = Label(root, text="", font=("Arial", 14), fg="#E30B94", bg="#E2EC1F")
setup_label.pack(pady=10) 


# LABEL TO DISPLAY JOKE PUNCHLINE
punchline_label = Label(root, text="", font=("Arial", 12), fg="yellow", bg="#E30B94")
punchline_label.pack(pady=5)


# BUTTON FOR RANDOM JOKE 
# BUTTON TO SHOW THE PUNCHLINE
btn_punchline = Button(root, text="Show Punchline", font=("Arial", 12), command=show_punchline, bg="#7CFC00", fg="black", activebackground="#32CD32", activeforeground="white")
btn_punchline.pack(pady=5)

# BUTTON TO LOAD ANOTHER RANDOM JOKE
btn_next = Button(root, text="Next Joke", font=("Arial", 12),command=next_joke, bg="#7CFC00", fg="black",activebackground="#32CD32", activeforeground="white")
btn_next.pack(pady=5)

#BUTTON TO CLOSE 
btn_quit = Button(root, text="Quit", font=("Arial", 12),command=root.destroy, bg="#7CFC00", fg="black",activebackground="#32CD32", activeforeground="white")
btn_quit.pack(pady=10)


tell_joke()
root.mainloop()
