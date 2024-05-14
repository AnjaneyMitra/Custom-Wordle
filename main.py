import random
import tkinter as tk
from tkinter import messagebox

# Constants
WORD_LENGTH = 5  # Length of the word to be guessed
MAX_ATTEMPTS = 10  # Maximum number of attempts allowed
COLORS = {
    "correct": "pink",
    "misplaced": "yellow",
    "incorrect": "gray"
}

# Function to load words from a file
def load_words(file_path):
    with open(file_path, "r") as file:
        words = [word.strip() for word in file.readlines()]
    return [word for word in words if len(word) == WORD_LENGTH]

# Function to check the guess
def check_guess(guess, target_word):
    result = []
    word_counts = {char: target_word.count(char) for char in set(target_word)}
    for i, char in enumerate(guess):
        if char == target_word[i]:
            result.append(COLORS["correct"])
            word_counts[char] -= 1
        elif char in target_word and word_counts[char] > 0:
            result.append(COLORS["misplaced"])
            word_counts[char] -= 1
        else:
            result.append(COLORS["incorrect"])
    return result
# GUI
root = tk.Tk()
root.title("Custom Wordle")

# Game state variables
word_list = load_words("words.txt")  # Load words from a file
target_word = random.choice(word_list)
attempts = []
current_attempt = 0

# Function to handle guess submission
def submit_guess(event=None):
    global current_attempt
    guess = guess_entry.get().lower()
    if len(guess) != WORD_LENGTH or guess not in word_list:
        messagebox.showerror("Invalid Guess", "Please enter a valid 5-letter word.")
        return
    attempts.append(guess)
    result = check_guess(guess, target_word)
    display_result(result)
    guess_entry.delete(0, tk.END)
    current_attempt += 1
    if guess == target_word:
        messagebox.showinfo("Congratulations!", f"You guessed the word '{target_word}' correctly!")
        reset_game()
    elif current_attempt == MAX_ATTEMPTS:
        messagebox.showinfo("Game Over", f"You ran out of attempts. The word was '{target_word}'.")
        reset_game()

# Function to display the result
def display_result(result):
    for i, char in enumerate(result):
        guess_labels[current_attempt][i].config(bg=char, fg="white" if char != "gray" else "black")

# Function to reset the game
def reset_game():
    global target_word, attempts, current_attempt
    target_word = random.choice(word_list)
    attempts = []
    current_attempt = 0
    for row in guess_labels:
        for label in row:
            label.config(bg="white", fg="black", text="")

# GUI components
guess_entry = tk.Entry(root, font=("Arial", 16))
guess_entry.bind("<Return>", submit_guess)
guess_entry.grid(row=0, column=0, columnspan=WORD_LENGTH, padx=5, pady=5)

guess_labels = [[tk.Label(root, font=("Arial", 16), width=2, height=1, bg="white", fg="black") for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)]
for i, row in enumerate(guess_labels):
    for j, label in enumerate(row):
        label.grid(row=i+1, column=j, padx=5, pady=5)

submit_button = tk.Button(root, text="Submit", font=("Arial", 14), command=submit_guess)
submit_button.grid(row=MAX_ATTEMPTS+1, column=0, columnspan=WORD_LENGTH, padx=5, pady=5)

root.mainloop()