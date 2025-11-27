
# IMPORTING REQUIRED LIBRARIES
from tkinter import * # import tkinter module
from PIL import ImageTk, Image # import pil module(for images)
import random # import random(for numbers)
import time# import time (for time)
 

# MAIN WINDOW SETUP
root = Tk() # Creates the output window
root.title("Math Quiz Game")# Creates a title in the output
root.geometry("800x600")# Creates a output Window of size 800 x 600
root.resizable(False, False)# Output Window size is fixed
def switch_to_frame(frame): # Function to switch between frames
    frame.tkraise()


# GAME VARIABLES
score = 0 # store player score
lives = 3# store player lives (starts with 3)
attempts = 0 # store number of wrong attempts for one question
correct_answer = None# store the correct answer for the current question
current_level = "" # store the selected level (easy,moderate, difficult)
question_count = 0# store how many questions have been asked
MAX_QUESTIONS = 5  # store total number of questions per level
lives_expired_time = None # store the time when lives reached zero
game_result = "" # store game result (won or lost)


# STARTING QUIZ FOR SELECTED LEVEL
def start_quiz(level):# creating a function named start_quiz that starts the quiz for selected level
    global score, lives, attempts, current_level, question_count, lives_expired_time # using global variables to track
     # checking if lives are locked
    if lives_expired_time:
        elapsed = time.time() - lives_expired_time  #calculating time passed since lives became zero
 # If less than 1 hour has passed
        if elapsed < 3600:
            feedback_label.config(text="⏳ Lives will refill in 1 hour")
            answer_entry.place_forget()    # Hides entry button if time passed is less than 1 hour
            submit_button.place_forget()   # Hide submit button if time passed is less tham 1 hour
            switch_to_frame(frame_quiz)
            return
        else:
            # After 1 hour passed, reset lives
            lives_expired_time = None
            lives = 3
    # Resetting game progress
    score = 0
    lives = 3
    attempts = 0
    question_count = 0
    current_level = level
    # Geting player name from entry box
    user_name = name_entry.get().strip()
    if not user_name:
        user_name = "Player"
   # Updating labels on the quiz screen
    name_label.config(text=f"Welcome, {user_name}")#display player name
    level_label.config(text=f"Level: {level}")#display level
    score_label.config(text=f"Score: {score}")#display score
    lives_label.config(text=f"Lives: {lives}")#display lives
    feedback_label.config(text="")#display feedback
   # displaying answer box and submit button
    answer_entry.place(x=300, y=260)
    submit_button.place(x=360, y=330)
   # Create first question
    generate_question()
   # Switch to quiz screen to display game
    switch_to_frame(frame_quiz)


#GENERATING QUESTION
def generate_question():# creating a function named generate_question that creates math question
    global correct_answer, attempts, question_count, game_result# using global variables for current answer, attempts, question count, and game result
    # Checking lives of the player
    if lives <= 0:
        game_result = "lost"#if the lives are zero then the game result is zero
        show_game_over()
        return

    # checking if questions are completed
    elif question_count >= MAX_QUESTIONS:
        game_result = "won"
        show_game_win()
        return

    # Create 2 random numbers and b for the question
    a = random.randint(1, 10)
    b = random.randint(1, 10)

    attempts = 0           # Reset wrong tries
    question_count += 1    # Increase question number

    # Generating questions based on difficulty level
#for easy level - addition questions
    if current_level == "Easy":
        question = f"{a} + {b} = ?"# function for addition of two random numbers a and b
        correct_answer = a + b
# for moderate level - multiplication questions
    elif current_level == "Moderate":
        question = f"{a} × {b} = ?"# function for multiplication of two random numbers a and b
        correct_answer = a * b
#for difficult level - division questions
    elif current_level == "Difficult":
        question = f"{a * b} ÷ {a} = ?"# function for division of two random numbers a and b
        correct_answer = b
# Displaying question on screen
    question_label.config(text=f"Q{question_count}: {question}")
# deleting old answers from entry box
    answer_entry.delete(0, END)


#CHECKING ANSWERS

def check_answer():# creating a function named check_answer that checks if the player's answer is correct or wrong
    global score, lives, attempts, game_result # using global variables for score, lives, attempts, and game result

    # Make sure player entered a number
    try:
        user_answer = int(answer_entry.get())# "Try" to get the answer from the entry box and convert it to an integer
    except ValueError:
        feedback_label.config(text="Enter a number.") # If the input is not a number, show THE  error message enter a number
        return
    #checking if the answers are correct
    if user_answer == correct_answer:
        score += 3 if attempts == 0 else 1 # user will get 3 points at first try and for second and third try 1 point
        feedback_label.config(text="✅ Correct!")# Show "Correct" feedback to the player
        score_label.config(text=f"Score: {score}")# Update the score label on the screen
        generate_question()  # Generate the next question
        return
    #if the answer is wrong
    attempts += 1 #increase the number of wrong attempts
    if attempts < 3:#if function hepls to Allow the player to try again if attempts are less than 3
        feedback_label.config(text=f"❌ Try again ({3 - attempts} left)")# show wrong answer message and remaining tries
        return
    lives -= 1  # If 3 wrong attemptsthen user will Lose 1 life 
    lives_label.config(text=f"Lives: {lives}")#Update the lives label on the screen
    if lives <= 0:#if function will check if the lives reached below zero
        game_result = "lost" #set game result to lost
        show_game_over()#display game over
        return
    feedback_label.config(text="⚠️ No points. Next question.")# display the feedback to the player
    generate_question()#Generate the next question


# GAME OVER SCREEN
def show_game_over():
    global lives_expired_time
    # Hide answer box and submit button
    answer_entry.place_forget()
    submit_button.place_forget()
    # Record time when lives became zero (start 1-hour lock)
    lives_expired_time = time.time()
    # Update game over screen text
    final_score_label.config(text=f"Final Score: {score}")
    final_lives_label.config(text="Lives: 0")
    lives_over_label.config(text="❌ Your lives are over!\n⏳ Please wait 1 hour to refill.")
    # Go to Game Over screen
    switch_to_frame(frame_gameover)


# GAME WIN SCREEN
def show_game_win():# creating a function named show_game_win that displays the Game Win screen when all questions are answered
    win_score_label.config(text=f"Score: {score}")#updates the score
    switch_to_frame(frame_gamewin) #switch to game win screen


# RESTART-BACK TO WELCOME SCREEN
def restart_game():# creating a function named restart_game that brings the player back to the welcome screen
    switch_to_frame(frame_welcome)#Switch to welcome screen.


# LOADING IMAGES FOR BACKGROUNDS
# Image.open() opens the image file 
# resize() changes it to fit the window (800x600)
# ImageTk.PhotoImage() converts the image so it can be displayed in Tkinter
bg_welcome = ImageTk.PhotoImage(Image.open("Assessment 1 - Skills Portfolio/Math quiz/images/mathquizwelcome.jpeg").resize((800, 600)))
bg_level   = ImageTk.PhotoImage(Image.open("Assessment 1 - Skills Portfolio/Math quiz/mathquizdiffculty.jpeg").resize((800, 600)))
bg_quiz    = ImageTk.PhotoImage(Image.open("Assessment 1 - Skills Portfolio/Math quiz/images/mathquiz1.jpeg").resize((800, 600)))
bg_gameover = ImageTk.PhotoImage(Image.open("Assessment 1 - Skills Portfolio/Math quiz/mathquizgameover.jpeg").resize((800, 600)))
bg_gamewin = ImageTk.PhotoImage(Image.open("Assessment 1 - Skills Portfolio/Math quiz/mathquizwin.jpeg").resize((800, 600)))


# FRAME 1: WELCOME SCREEN
frame_welcome = Frame(root, width=800, height=600)#create a frame for the welcome screen with width 800 and height 600
Label(frame_welcome, image=bg_welcome).place(x=0, y=0, relwidth=1, relheight=1)#adding the background image
Label(frame_welcome, text="Enter your name:", font=("poppins", 12), fg="black").place(x=340, y=380)#createn lable called  enter your name
name_entry = Entry(frame_welcome, font=("poppins", 12), bg="green")# create an entry box for the player to type their name
name_entry.place(x=335, y=410)#position of the entry box
Button(frame_welcome, text="Start", font=("poppins", 12), bg="#0ABBF7", fg="yellow",command=lambda: switch_to_frame(frame_level)).place(x=390, y=470)# create a Start button that switches to the level selection frame when clicked
frame_welcome.place(x=0, y=0, width=800, height=600)

# FRAME 2: DIFFICULTY SELECTION SCREEN

frame_level = Frame(root, width=800, height=600)  # create a frame for the difficulty selection screen
Label(frame_level, image=bg_level).place(x=0, y=0, relwidth=1, relheight=1)  # adding the background image
# Easy button
Button(frame_level, text="Easy", font=("poppins", 12), bg="#2E80E5", fg="black", command=lambda: start_quiz("Easy")).place(x=360, y=330)
# Moderate button (fixed — now starts Moderate)
Button(frame_level, text="Moderate", font=("poppins", 12), bg="#2E80E5", fg="black",command=lambda: start_quiz("Moderate")).place(x=360, y=280)
# Difficult button (restored — you deleted it before)
Button(frame_level, text="Difficult", font=("poppins", 12), bg="#2E80E5", fg="black",command=lambda: start_quiz("Difficult")).place(x=360, y=230)
# Back button
Button(frame_level, text="Back", font=("poppins", 12), bg="#2E80E5", fg="black",command=lambda: switch_to_frame(frame_welcome)).place(x=360, y=500)
frame_level.place(x=0, y=0, width=800, height=600)


# FRAME 3: QUIZ SCREEN
frame_quiz = Frame(root, width=800, height=600)#create a frame for the quiz screen with width 800 and height 60
Label(frame_quiz, image=bg_quiz).place(x=0, y=0, relwidth=1, relheight=1)#adding the background image
name_label = Label(frame_quiz, text="", font=("poppins", 12),  fg="black")#creating  label showing the player's name during quiz
name_label.place(x=130, y=60)#Position of name label
level_label = Label(frame_quiz, text="", font=("poppins", 12),  fg="black")# create label showing the chosen difficulty level
level_label.place(x=130, y=150)#position of level label
score_label = Label(frame_quiz, text="Score: 0", font=("poppins", 12),  fg="black")#create label showing the player's current score
score_label.place(x=130, y=90)#position of score label
lives_label = Label(frame_quiz, text="Lives: 3", font=("poppins", 12), fg="black")#create label showing how many lives are left
lives_label.place(x=130, y=120)#position of lives label
question_label = Label(frame_quiz, text="", font=("poppins", 14), bg="#B5B94C", fg="black")#create label where the math question is displayed
question_label.place(x=340, y=180)#position of question label
answer_entry = Entry(frame_quiz, font=("poppins", 12))#creates entry box where player types the answer
answer_entry.place(x=300, y=260)#position of entry box
submit_button = Button(frame_quiz, text="Submit", font=("poppins", 12), bg="#2E80E5", fg="black", command=check_answer)#create submit button used to check the player's answer
submit_button.place(x=360, y=330)#position of submit button
feedback_label = Label(frame_quiz, text="", font=("poppins", 12), fg="black")#creates label used to show feedback messages correct and wrong)
feedback_label.place(x=340, y=400)#postion of feedback label
Button(frame_quiz, text="Back", font=("poppins", 12), bg="#2E80E5", fg="yellow",command=lambda: switch_to_frame(frame_level)).place(x=360, y=460)#creates back button to return to level selection screen
frame_quiz.place(x=0, y=0, width=800, height=600)#position of back button



# FRAME 4: GAME OVER SCREEN
frame_gameover = Frame(root, width=800, height=600)# create the Game Over frame
Label(frame_gameover, image=bg_gameover).place(x=0, y=0, relwidth=1, relheight=1)# adding the background image
Label(frame_gameover, text="Better luck next time!", font=("poppins", 12), bg="#B5320A", fg="yellow").place(x=330, y=300)
final_score_label = Label(frame_gameover, text="", font=("poppins", 12), bg="#B5320A", fg="yellow")#create final score label
final_score_label.place(x=320, y=180)#postion of final score label
final_lives_label = Label(frame_gameover, text="", font=("poppins", 12), bg="#B5320A", fg="yellow")#create final lives label
final_lives_label.place(x=320, y=210)#position of final lives
lives_over_label = Label(frame_gameover, text="", font=("poppins", 12), bg="#B5320A", fg="white", justify="center")#creating lives over label
lives_over_label.place(x=320, y=240)#position of lives over label
Button(frame_gameover, text="Play Again", font=("poppins", 12), bg="#2E80E5", fg="yellow",command=restart_game).place(x=360, y=460)#create play agin button
frame_gameover.place(x=0, y=0, width=800, height=600)#positon of gameover button


# FRAME 5: GAME WIN SCREEN
frame_gamewin = Frame(root, width=800, height=600)#create game win frame
Label(frame_gamewin, image=bg_gamewin).place(x=0, y=0, relwidth=1, relheight=1)#adding background
Label(frame_gamewin, text="🎉 Level Complete!", font=("poppins", 16), bg="#00AE3D", fg="white").place(x=330, y=260)
Label(frame_gamewin, text="Great job finishing all questions!", font=("poppins", 12), bg="#00AE3D", fg="white").place(x=330, y=300)#disaply the text
win_score_label = Label(frame_gamewin, text="", font=("poppins", 12), bg="#00AE3D", fg="yellow")#create win score label display the winning score of the player
win_score_label.place(x=360, y=360)#position of win score label
Button(frame_gamewin, text="Continue", font=("poppins", 12), bg="#2E80E5", fg="yellow", command=lambda: switch_to_frame(frame_level)).place(x=360, y=460)#creates continue button to return to level selection screen
frame_gamewin.place(x=0, y=0, width=800, height=600)#position of continue button


# STARTING THE GAME
switch_to_frame(frame_welcome)# Show welcome screen first
root.mainloop() # Runs the game 



