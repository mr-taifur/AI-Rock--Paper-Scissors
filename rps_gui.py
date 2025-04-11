import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import threading
import os
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects
win_sound = pygame.mixer.Sound("win_sound.wav")  # Replace with your own sound file
lose_sound = pygame.mixer.Sound("lose_sound.wav")
draw_sound = pygame.mixer.Sound("draw_sound.wav")

# Game State
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
ai_score = 0
history = []

# Function to determine winner
def get_winner(player, ai):
    if player == ai:
        return "Draw"
    elif (player == "Rock" and ai == "Scissors") or \
         (player == "Paper" and ai == "Rock") or \
         (player == "Scissors" and ai == "Paper"):
        return "Player"
    else:
        return "AI"

# Countdown animation + game logic
def play(player_choice):
    countdown_label.config(text="Rock...")
    window.update()
    time.sleep(0.4)
    countdown_label.config(text="Paper...")
    window.update()
    time.sleep(0.4)
    countdown_label.config(text="Scissors...")
    window.update()
    time.sleep(0.4)
    countdown_label.config(text="Shoot!")
    window.update()
    time.sleep(0.3)

    ai_choice = random.choice(choices)
    winner = get_winner(player_choice, ai_choice)

    global player_score, ai_score
    if winner == "Player":
        result_label.config(text="🎉 You Win!", fg="green")
        player_score += 1
        win_sound.play()  # Play the win sound
    elif winner == "AI":
        result_label.config(text="💻 AI Wins!", fg="red")
        ai_score += 1
        lose_sound.play()  # Play the lose sound
    else:
        result_label.config(text="🤝 Draw!", fg="blue")
        draw_sound.play()  # Play the draw sound

    player_choice_label.config(text=f"You chose: {player_choice}")
    ai_choice_label.config(text=f"AI chose: {ai_choice}")
    score_label.config(text=f"Score — You: {player_score} | AI: {ai_score}")
    history.append(f"You: {player_choice} | AI: {ai_choice} → {winner}")
    history_text.set("\n".join(history[-5:]))

# Threaded play to avoid GUI freeze
def threaded_play(player_choice):
    threading.Thread(target=play, args=(player_choice,)).start()

# Reset game state
def reset_game():
    global player_score, ai_score, history
    player_score = 0
    ai_score = 0
    history = []
    result_label.config(text="")
    player_choice_label.config(text="")
    ai_choice_label.config(text="")
    score_label.config(text="Score — You: 0 | AI: 0")
    history_text.set("")
    countdown_label.config(text="")

# Save leaderboard
def save_leaderboard():
    with open("leaderboard.txt", "a") as file:
        file.write(f"Player Score: {player_score} | AI Score: {ai_score}\n")

# Load leaderboard
def load_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            leaderboard = file.readlines()
        return leaderboard
    except FileNotFoundError:
        return []

# Show leaderboard in a pop-up
def show_leaderboard():
    leaderboard = load_leaderboard()
    leaderboard_text = "\n".join(leaderboard[-5:])  # Show the last 5 scores
    leaderboard_window = tk.Toplevel(window)
    leaderboard_window.title("Leaderboard")
    leaderboard_label = tk.Label(leaderboard_window, text=leaderboard_text, font=("Courier", 12), justify="left")
    leaderboard_label.pack(pady=20)

# Load and resize image with fallback
def load_image(name):
    try:
        img = Image.open(name)
        print(f"✅ Loaded {name}")
        return ImageTk.PhotoImage(img.resize((100, 100)))
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
        return None

# Function to toggle theme
def toggle_theme():
    current_bg = window.cget("bg")
    if current_bg == "#e8f0fe":  # Light theme
        window.configure(bg="#333333")
        title.config(bg="#333333", fg="white")
        result_label.config(bg="#333333", fg="white")
        countdown_label.config(bg="#333333", fg="white")
        player_choice_label.config(bg="#333333", fg="white")
        ai_choice_label.config(bg="#333333", fg="white")
        score_label.config(bg="#333333", fg="white")
        history_box.config(bg="#333333", fg="white")
        leaderboard_btn.config(bg="#444444", fg="white")
        reset_btn.config(bg="#444444", fg="white")
    else:  # Dark theme
        window.configure(bg="#e8f0fe")
        title.config(bg="#e8f0fe", fg="black")
        result_label.config(bg="#e8f0fe", fg="black")
        countdown_label.config(bg="#e8f0fe", fg="gray")
        player_choice_label.config(bg="#e8f0fe", fg="black")
        ai_choice_label.config(bg="#e8f0fe", fg="black")
        score_label.config(bg="#e8f0fe", fg="black")
        history_box.config(bg="#e8f0fe", fg="black")
        leaderboard_btn.config(bg="#f2f2f2", fg="black")
        reset_btn.config(bg="#f2f2f2", fg="black")

# GUI setup
window = tk.Tk()
window.title("Rock Paper Scissors - Deluxe")
window.geometry("500x620")
window.configure(bg="#e8f0fe")

title = tk.Label(window, text="Rock, Paper, Scissors", font=("Helvetica", 20, "bold"), bg="#e8f0fe")
title.pack(pady=10)

# Load images
rock_img = load_image("rock.png")
paper_img = load_image("paper.png")
scissors_img = load_image("scissors.png")

# Buttons with images
button_frame = tk.Frame(window, bg="#e8f0fe")
button_frame.pack(pady=15)

btn_style = {
    "bd": 3,
    "relief": tk.RAISED,
    "bg": "#d0e1ff",
    "activebackground": "#aacbff",
    "cursor": "hand2"
}

rock_btn = tk.Button(button_frame, image=rock_img, command=lambda: threaded_play("Rock"), **btn_style)
rock_btn.image = rock_img
rock_btn.grid(row=0, column=0, padx=15)

paper_btn = tk.Button(button_frame, image=paper_img, command=lambda: threaded_play("Paper"), **btn_style)
paper_btn.image = paper_img
paper_btn.grid(row=0, column=1, padx=15)

scissors_btn = tk.Button(button_frame, image=scissors_img, command=lambda: threaded_play("Scissors"), **btn_style)
scissors_btn.image = scissors_img
scissors_btn.grid(row=0, column=2, padx=15)

# Game output
countdown_label = tk.Label(window, text="", font=("Helvetica", 14), bg="#e8f0fe", fg="gray")
countdown_label.pack(pady=5)

player_choice_label = tk.Label(window, text="", font=("Helvetica", 12), bg="#e8f0fe")
player_choice_label.pack()

ai_choice_label = tk.Label(window, text="", font=("Helvetica", 12), bg="#e8f0fe")
ai_choice_label.pack()

result_label = tk.Label(window, text="", font=("Helvetica", 16, "bold"), bg="#e8f0fe")
result_label.pack(pady=10)

score_label = tk.Label(window, text="Score — You: 0 | AI: 0", font=("Helvetica", 12), bg="#e8f0fe")
score_label.pack(pady=5)

# Match history
tk.Label(window, text="🕹️ Last 5 Rounds:", font=("Helvetica", 12, "bold"), bg="#e8f0fe").pack(pady=(10, 0))
history_text = tk.StringVar()
history_box = tk.Label(window, textvariable=history_text, font=("Courier", 10), bg="#e8f0fe", justify="left")
history_box.pack()

# Reset button
reset_btn = tk.Button(window, text="🔁 Reset Game", font=("Helvetica", 12), command=reset_game, bg="#f2f2f2", cursor="hand2")
reset_btn.pack(pady=15)

# Leaderboard button
leaderboard_btn = tk.Button(window, text="🏆 View Leaderboard", font=("Helvetica", 12), command=show_leaderboard, bg="#f2f2f2", cursor="hand2")
leaderboard_btn.pack(pady=15)

# Theme toggle button
theme_toggle_btn = tk.Button(window, text="🌙 Dark Mode", font=("Helvetica", 12), command=toggle_theme, bg="#f2f2f2", cursor="hand2")
theme_toggle_btn.pack(pady=10)

# Start GUI loop
window.mainloop()
