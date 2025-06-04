
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from PIL import ImageGrab

def extract_features(password):
    return [
        len(password),
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ]

passwords = [
    ("password", 0),
    ("Password123", 1),
    ("Pass123!", 2),
    ("P@ssw0rd2023", 3),
    ("Str0ng!Pass#2023", 4),
]
X = [extract_features(pw) for pw, _ in passwords]
y = [label for _, label in passwords]

clf = RandomForestClassifier()
clf.fit(X, y)

def evaluate_password_strength(pw):
    features = np.array([extract_features(pw)])
    strength = clf.predict(features)[0]
    return strength

def get_strength_label(level):
    return ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][level]

def get_strength_color(level):
    return ["red", "orange", "yellow", "lightgreen", "green"][level]

def update_strength_bar(strength):
    strength_bar['value'] = (strength + 1) * 20
    strength_bar.configure(style=f"{get_strength_color(strength)}.Horizontal.TProgressbar")
    strength_label.config(text=get_strength_label(strength), foreground=get_strength_color(strength))

def check_password():
    pw = password_entry.get()
    if not pw:
        messagebox.showwarning("Input Required", "Please enter a password to evaluate.")
        return
    strength = evaluate_password_strength(pw)
    update_strength_bar(strength)
    feedback.config(text=f"Password Feedback:\n• {get_strength_label(strength)}\n• Use upper & lowercase, numbers, symbols.\n• Avoid dictionary words.")

def generate_password():
    length = random.randint(10, 16)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    check_password()

def plot_graph():
    levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    counts = [sum(1 for _, s in passwords if s == i) for i in range(5)]
    plt.bar(levels, counts, color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
    plt.title("Password Strength Distribution")
    plt.xlabel("Strength Level")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("password_strength_graph.png")
    plt.show()

def capture_screenshot():
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    x1 = x + root.winfo_width()
    y1 = y + root.winfo_height()
    img = ImageGrab.grab().crop((x, y, x1, y1))
    img.save("gui_dashboard_screenshot.png")
    messagebox.showinfo("Screenshot Saved", "Dashboard screenshot saved as gui_dashboard_screenshot.png.")

root = tk.Tk()
root.title("Password Strength Evaluator with ML")
root.geometry("600x400")
style = ttk.Style()
for color in ["red", "orange", "yellow", "lightgreen", "green"]:
    style.configure(f"{color}.Horizontal.TProgressbar", troughcolor='white', background=color)

tk.Label(root, text="Enter Password or Generate One:", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, width=40, font=("Arial", 12))
password_entry.pack(pady=5)

ttk.Button(root, text="Evaluate Password", command=check_password).pack(pady=5)
ttk.Button(root, text="Generate Strong Password", command=generate_password).pack(pady=5)

strength_bar = ttk.Progressbar(root, length=300, maximum=100, value=0)
strength_bar.pack(pady=10)
strength_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
strength_label.pack()

feedback = tk.Label(root, text="", font=("Arial", 10), justify="left")
feedback.pack(pady=10)

ttk.Button(root, text="Plot Strength Graph", command=plot_graph).pack(pady=5)
ttk.Button(root, text="Capture Dashboard Screenshot", command=capture_screenshot).pack(pady=5)

root.mainloop()
