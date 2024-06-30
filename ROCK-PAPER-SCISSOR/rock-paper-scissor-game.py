import tkinter as tk
from tkinter import messagebox
import random

# Initialize main window
root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("500x600")
root.configure(bg="#001f3f")

# Global variables for the score and history
user_score = 0
computer_score = 0
user_history = []
computer_history = []
games_played = 0
user_turn = True

# Choices
choices = ["Rock", "Paper", "Scissors"]

def play(user_choice):
    global user_score, computer_score, games_played, user_turn
    if not user_turn:
        messagebox.showinfo("Wait", "Please wait for your turn!")
        return

    user_turn = False
    computer_choice = random.choice(choices)
    games_played += 1
    
    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = f"You win! Computer chose {computer_choice}."
        user_score += 1
    else:
        result = f"You lose! Computer chose {computer_choice}."
        computer_score += 1
    
    user_history.append(user_choice)
    computer_history.append(computer_choice)
    if len(user_history) > 5:
        user_history.pop(0)
        computer_history.pop(0)
    
    update_score()
    update_history()
    update_statistics()
    messagebox.showinfo("Result", result)
    user_turn = True

def update_score():
    score_label.config(text=f"User: {user_score}  Computer: {computer_score}")

def update_history():
    user_history_label.config(text=f"User History: {', '.join(user_history)}")
    computer_history_label.config(text=f"Computer History: {', '.join(computer_history)}")

def update_statistics():
    if games_played == 0:
        user_win_percentage = 0
        computer_win_percentage = 0
    else:
        user_win_percentage = (user_score / games_played) * 100
        computer_win_percentage = (computer_score / games_played) * 100

    statistics_label.config(text=f"Games Played: {games_played}\n"
                                 f"User Win %: {user_win_percentage:.2f}%\n"
                                 f"Computer Win %: {computer_win_percentage:.2f}%")

def reset_game():
    global user_score, computer_score, user_history, computer_history, games_played, user_turn
    user_score = 0
    computer_score = 0
    user_history = []
    computer_history = []
    games_played = 0
    user_turn = True
    update_score()
    update_history()
    update_statistics()

# GUI elements
title_label = tk.Label(root, text="Rock Paper Scissors", font=("Arial", 30, "bold"), bg="#001f3f", fg="white")
title_label.pack(pady=20)

score_frame = tk.Frame(root, bg="#001f3f")
score_frame.pack(pady=10)

score_label = tk.Label(score_frame, text=f"User: {user_score}  Computer: {computer_score}", font=("Arial", 18, "bold"), bg="#001f3f", fg="white")
score_label.grid(row=0, column=0, pady=10)

frame = tk.Frame(root, bg="#001f3f")
frame.pack(pady=20)

rock_button = tk.Button(frame, text="Rock", font=("Arial", 18, "bold"), bg="#FF4136", fg="white", command=lambda: play("Rock"))
rock_button.grid(row=0, column=0, padx=10)

paper_button = tk.Button(frame, text="Paper", font=("Arial", 18, "bold"), bg="#2ECC40", fg="white", command=lambda: play("Paper"))
paper_button.grid(row=0, column=1, padx=10)

scissors_button = tk.Button(frame, text="Scissors", font=("Arial", 18, "bold"), bg="#0074D9", fg="white", command=lambda: play("Scissors"))
scissors_button.grid(row=0, column=2, padx=10)

history_frame = tk.Frame(root, bg="#001f3f")
history_frame.pack(pady=10)

user_history_label = tk.Label(history_frame, text="User History: ", font=("Arial", 14), bg="#001f3f", fg="white")
user_history_label.grid(row=0, column=0, pady=5)

computer_history_label = tk.Label(history_frame, text="Computer History: ", font=("Arial", 14), bg="#001f3f", fg="white")
computer_history_label.grid(row=1, column=0, pady=5)

statistics_frame = tk.Frame(root, bg="#001f3f")
statistics_frame.pack(pady=10)

statistics_label = tk.Label(statistics_frame, text="Games Played: 0\nUser Win %: 0.00%\nComputer Win %: 0.00%", font=("Arial", 14), bg="#001f3f", fg="white", justify="left")
statistics_label.grid(row=0, column=0, pady=10)

reset_button = tk.Button(root, text="Reset Game", font=("Arial", 18, "bold"), bg="#FF851B", fg="white", command=reset_game)
reset_button.pack(pady=20)

# Run the application
root.mainloop()