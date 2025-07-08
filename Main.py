import tkinter as tk
from functools import partial
import os
from PIL import Image, ImageTk

player_name = "Player"

leaderboard_data = [
    ("Bob", 1200),
    ("jeff", 1100),
    ("Archangel", 1000),
    ("Daisy", 550),
    ("Ethan", 500),
    ("Ella", 350),
    ("Martin", 250),
    ("Josh", 150),
]

# Icon paths + minimum score thresholds for display
ICON_PATHS = {
    1: (r"C:\Users\abell\PycharmProjects\PythonProject3\Demon.png", 1200),
    2: (r"C:\Users\abell\PycharmProjects\PythonProject3\Emoji_Icon_-_Sunglasses_cool_emoji.png", 1100),
    3: (r"C:\Users\abell\PycharmProjects\PythonProject3\Happy.png", 1000),
}

RESIZED_ICONS = {}

def load_resized_icons(master):
    for idx, (path, _) in ICON_PATHS.items():
        if os.path.isfile(path):
            img = Image.open(path)
            img.thumbnail((80, 50))  # Resize, keep ratio
            RESIZED_ICONS[idx] = ImageTk.PhotoImage(img, master=master)
        else:
            RESIZED_ICONS[idx] = None

def open_clicker_window(player: str):
    global leaderboard_data
    click_count = 999

    if not any(name == player for name, _ in leaderboard_data):
        leaderboard_data.append((player, 0))

    clicker = tk.Tk()
    clicker.title("Clicker Leaderboard")
    clicker.geometry("360x580")
    clicker.configure(bg="#f0f0f0")

    load_resized_icons(clicker)

    title_label = tk.Label(clicker, text=f"Clicks: {click_count}", font=("Arial", 14), bg="#f0f0f0")
    title_label.pack(pady=10)

    board_frame = tk.Frame(clicker, bg="#f0f0f0")
    board_frame.pack(fill="both", expand=True, padx=10)

    # Load button icons to cycle through
    button_images = []
    button_image_paths = [
        r"\PycharmProjects\PythonProject3\Jeff1.png",
        r"\PycharmProjects\PythonProject3\Jeff2.png",
        r"\PycharmProjects\PythonProject3\Jeff3.png",
    ]
    for path in button_image_paths:
        if os.path.isfile(path):
            img = Image.open(path)
            img.thumbnail((500, 500))
            button_images.append(ImageTk.PhotoImage(img, master=clicker))
    if not button_images:
        button_images = [None]  # fallback, no images found

    button_image_index = 0

    def update_leaderboard():
        nonlocal click_count
        for i, (n, s) in enumerate(leaderboard_data):
            if n == player:
                leaderboard_data[i] = (n, click_count)
        leaderboard_data.sort(key=lambda x: x[1], reverse=True)

    def render_leaderboard():
        for widget in board_frame.winfo_children():
            widget.destroy()

        # TOP 3 with icons only if scores meet thresholds
        for idx, (n, s) in enumerate(leaderboard_data[:3], start=1):
            row = tk.Frame(board_frame, bg="#f0f0f0")
            row.pack(fill="x", pady=2)

            icon_img = RESIZED_ICONS.get(idx)
            required_score = ICON_PATHS.get(idx)[1]

            if icon_img and s >= required_score:
                tk.Label(row, image=icon_img, bg="#f0f0f0").pack(side="left", padx=(0, 5))
            else:
                tk.Label(row, width=5, bg="#f0f0f0").pack(side="left")  # empty space

            tk.Label(row, text=f"{idx}. {n} — {s}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side="left")

        # Separator
        tk.Frame(board_frame, height=2, bd=1, relief="sunken", bg="#999").pack(fill="x", pady=5)

        # Rest of leaderboard
        for idx, (n, s) in enumerate(leaderboard_data[3:], start=4):
            tk.Label(board_frame, text=f"{idx}. {n} — {s}", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=1)

    def on_click():
        nonlocal click_count, button_image_index
        click_count += 1
        title_label.config(text=f"Clicks: {click_count}")

        # Cycle button image on each click
        button_image_index = (button_image_index + 1) % len(button_images)
        btn.config(image=button_images[button_image_index])

        update_leaderboard()
        render_leaderboard()

    btn = tk.Button(clicker, text="Click Me!", font=("Arial", 12), command=on_click)
    btn.pack(pady=10)

    # Set initial button image if available
    if button_images[0]:
        btn.config(image=button_images[0])
        btn.image = button_images[0]  # keep reference

    # Initial render
    update_leaderboard()
    render_leaderboard()

    clicker.mainloop()

def validate_login(username_var, pw_var, cp_var, win, error_label):
    user = username_var.get().strip()
    pw = pw_var.get()
    cp = cp_var.get()

    if not user:
        error_label.config(text="Username cannot be empty", fg="red")
        return
    if pw != cp:
        error_label.config(text="Passwords do not match", fg="red")
        return

    global player_name
    player_name = user
    win.destroy()
    open_clicker_window(user)

def password_window():
    login = tk.Tk()
    login.title("Login")
    login.geometry("350x200")
    login.configure(bg="#f0f0f0")

    tk.Label(login, text="Username", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
    username_var = tk.StringVar()
    tk.Entry(login, textvariable=username_var).grid(row=0, column=1)

    tk.Label(login, text="Password", bg="#f0f0f0").grid(row=1, column=0)
    password_var = tk.StringVar()
    tk.Entry(login, textvariable=password_var, show="*").grid(row=1, column=1)

    tk.Label(login, text="Confirm Password", bg="#f0f0f0").grid(row=2, column=0)
    confirm_var = tk.StringVar()
    tk.Entry(login, textvariable=confirm_var, show="*").grid(row=2, column=1)

    error_label = tk.Label(login, text="", fg="red", bg="#f0f0f0")
    error_label.grid(row=4, column=0, columnspan=2)

    login_btn = partial(validate_login, username_var, password_var, confirm_var, login, error_label)
    tk.Button(login, text="Login", command=login_btn).grid(row=3, column=0, columnspan=2, pady=10)

    login.mainloop()

if __name__ == "__main__":
    password_window()


