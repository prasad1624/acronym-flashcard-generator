import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

ACRONYMS_FILE = "acronyms.txt"


class FlashcardApp:
    def __init__(self, root, acronyms_file=ACRONYMS_FILE):
        self.root = root
        self.root.title("Acronym Flashcards")

        # FULLSCREEN
        root.attributes("-fullscreen", True)

        self.acronyms_file = acronyms_file
        self.all_cards = self.load_acronyms(self.acronyms_file)

        if not self.all_cards:
            messagebox.showerror("Error", "No acronyms found.")
            root.destroy()
            return

        self.session_cards = []
        self.index = 0
        self.revealed = False
        self.finished = False  # <-- NEW

        self.build_ui()
        self.start_new_session(randomize=True)

        # KEY BINDINGS
        root.bind("<Escape>", lambda e: self.exit_fullscreen())
        root.bind("<F11>", lambda e: self.toggle_fullscreen())
        root.bind("<space>", lambda e: self.reveal_card())
        root.bind("<Right>", lambda e: self.next_card())
        root.bind("<Left>", lambda e: self.prev_card())

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    def load_acronyms(self, path):
        if not os.path.exists(path):
            return []

        cards = []
        card_id = 1

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(None, 1)
                if len(parts) == 1:
                    acronym = parts[0]
                    meaning = ""
                else:
                    acronym, meaning = parts[0], parts[1]

                cards.append({"id": card_id, "acronym": acronym, "meaning": meaning})
                card_id += 1

        return cards

    # -----------------------------
    # BUILD UI
    # -----------------------------
    def build_ui(self):
        pad = 20
        main_frame = ttk.Frame(self.root, padding=pad)
        main_frame.pack(fill="both", expand=True)

        # Acronym Label
        self.acronym_var = tk.StringVar()
        self.acronym_label = tk.Label(
            main_frame,
            textvariable=self.acronym_var,
            font=("Helvetica", 72, "bold"),
            wraplength=1300,
            justify="center",
            cursor="hand2"
        )
        self.acronym_label.pack(pady=40)
        self.acronym_label.bind("<Button-1>", lambda e: self.reveal_card())

        # Meaning Label
        self.fullform_var = tk.StringVar()
        self.fullform_label = tk.Label(
            main_frame,
            textvariable=self.fullform_var,
            font=("Helvetica", 32),
            wraplength=1400,
            justify="center"
        )
        self.fullform_label.pack(pady=20)

        # RESTART BUTTON (hidden until finished)
        self.restart_btn = tk.Button(
            main_frame,
            text="RESTART",
            font=("Helvetica", 32, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            command=lambda: self.start_new_session(True)
        )
        self.restart_btn.pack(pady=40)
        self.restart_btn.pack_forget()  # hide initially

        # Progress
        self.progress_label = ttk.Label(self.root, font=("Helvetica", 16))
        self.progress_label.pack(pady=10)

        # Tips
        tip = (
            "RIGHT → Next | LEFT → Previous | SPACE → Reveal | "
            "Click acronym → Reveal | ESC → Exit Fullscreen"
        )
        self.tip_label = ttk.Label(self.root, text=tip, font=("Helvetica", 12))
        self.tip_label.pack(pady=10)

    # -----------------------------
    # SESSION
    # -----------------------------
    def start_new_session(self, randomize=True):
        self.restart_btn.pack_forget()
        self.session_cards = self.all_cards.copy()
        if randomize:
            random.shuffle(self.session_cards)

        self.index = 0
        self.revealed = False
        self.finished = False
        self.show_card()

    # -----------------------------
    # CARD LOGIC
    # -----------------------------
    def update_progress(self):
        if self.finished:
            self.progress_label.config(text="")
            return

        total = len(self.session_cards)
        current = self.index + 1
        self.progress_label.config(text=f"{current} / {total}")

    def show_finished_screen(self):
        """Display FINISHED screen + restart button."""
        self.acronym_var.set("FINISHED!")
        self.fullform_var.set("You have completed all flashcards.")
        self.finished = True
        self.restart_btn.pack()  # show restart button

    def show_card(self):
        if self.index >= len(self.session_cards):
            self.show_finished_screen()
            return

        card = self.session_cards[self.index]
        self.acronym_var.set(card["acronym"])
        self.fullform_var.set("Press SPACE or click to reveal meaning")
        self.revealed = False
        self.update_progress()

    def reveal_card(self):
        if self.finished:
            return

        meaning = self.session_cards[self.index]["meaning"]
        if meaning.strip() == "":
            meaning = "(No meaning available)"

        self.fullform_var.set(meaning)
        self.revealed = True

    def next_card(self):
        if self.finished:
            return  # prevent moving after finish

        self.index += 1
        if self.index >= len(self.session_cards):
            self.show_finished_screen()
        else:
            self.show_card()

    def prev_card(self):
        if self.finished:
            return

        self.index -= 1
        if self.index < 0:
            self.index = len(self.session_cards) - 1

        self.show_card()

    # -----------------------------
    # FULLSCREEN CONTROLS
    # -----------------------------
    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)


def main():
    root = tk.Tk()
    FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
