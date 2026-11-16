"""
Midnight Manor Mystery - A Tkinter Detective Game
Demonstrating Core Python and Tkinter Foundations
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
from db import DatabaseManager, save_db_config


class DetectiveGame:
    def __init__(self, root: tk.Tk):
        # ----------------------------------------------------
        # Tkinter Checklist: 1. Main window setup - Tk()
        # ----------------------------------------------------
        self.root = root
        self.root.title("Midnight Manor: Detective Case #1")
        self.root.geometry("860x680")
        self.root.minsize(800, 600)
        self.root.configure(bg="#111827")  # Deep slate background

        # ----------------------------------------------------
        # Python Checklist: 1. Variables and Data Types
        # Tkinter Checklist: 10. Tkinter Variables (StringVar, IntVar)
        # ----------------------------------------------------
        self.player_name_var = tk.StringVar(value="Holmes")
        self.score_var = tk.IntVar(value=100)
        self.level_var = tk.IntVar(value=1)
        self.status_var = tk.StringVar(value="Status: Ready to investigate")
        self.selected_suspect_var = tk.StringVar(value="")
        self.db_status_var = tk.StringVar(value="MySQL: Checking...")

        self.save_file_path = os.path.join(os.path.dirname(__file__), "savegame.json")
        self.db = DatabaseManager()

        # ----------------------------------------------------
        # Python Checklist: 3. Lists
        # ----------------------------------------------------
        self.discovered_clues = []
        self.questioned_suspects = []

        # ----------------------------------------------------
        # Python Checklist: 4. Dictionaries (Suspects & Clues)
        # ----------------------------------------------------
        self.suspects = {
            "Jenkins (The Butler)": {
                "name": "Jenkins",
                "motive": "Severe gambling debts reported by the village pub.",
                "alibi": "Polishing silver alone in the pantry from 9:30 to 10:30 PM.",
                "evidence_found": "Silver polish rag is completely dry and unused.",
                "is_guilty": False,
            },
            "Lady Beatrice (The Heiress)": {
                "name": "Lady Beatrice",
                "motive": "Recently written out of Lord Harrington's fortune.",
                "alibi": "Claims she was reading poetry in the conservatory.",
                "evidence_found": "Torn purple velvet scrap matching her missing glove was found on the safe lock.",
                "is_guilty": True,
            },
            "Prof. Sterling (The Scholar)": {
                "name": "Prof. Sterling",
                "motive": "Obsessed with ancient gemstones and ancient history.",
                "alibi": "Reviewing excavation maps in the guest library.",
                "evidence_found": "Magnifying glass and manor blueprints found in his briefcase.",
                "is_guilty": False,
            },
        }

        self.clues = {
            "The Safe Lock": {
                "desc": "Examined the safe lock. It was picked with a fine hair needle; a purple velvet fabric thread was trapped inside.",
                "bonus": 25,
            },
            "Muddy Footprints": {
                "desc": "Found size 5 delicate shoe prints tracking garden dirt from the conservatory into the study.",
                "bonus": 20,
            },
            "Broken Clock": {
                "desc": "The study grandfather clock is frozen at exactly 10:05 PM due to an electric short circuit.",
                "bonus": 15,
            },
            "Mysterious Letter": {
                "desc": "A torn note near the fireplace: '...bring the emerald to the garden gate before midnight.'",
                "bonus": 20,
            },
        }

        # ----------------------------------------------------
        # Tkinter Checklist: 4. Frames (Screen containers)
        # ----------------------------------------------------
        self.home_frame = None
        self.play_frame = None

        # Build initial screen
        self.create_home_screen()

    # ========================================================
    # SCREEN 1: HOME SCREEN
    # ========================================================
    def create_home_screen(self):
        """Builds the main entry / home screen using Frames, Labels, and Buttons."""
        if self.play_frame:
            self.play_frame.destroy()

        self.home_frame = tk.Frame(self.root, bg="#0f172a", padx=30, pady=30)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

        # Tkinter Checklist: 2. Labels
        title_label = tk.Label(
            self.home_frame,
            text="🕵️ MIDNIGHT MANOR MYSTERY",
            font=("Georgia", 26, "bold"),
            fg="#facc15",
            bg="#0f172a",
        )
        title_label.pack(pady=(35, 10))

        subtitle_label = tk.Label(
            self.home_frame,
            text="The Midnight Emerald has vanished from Lord Harrington's private study.\nCan you piece together the clues and unmask the culprit?",
            font=("Helvetica", 12),
            fg="#e2e8f0",
            bg="#0f172a",
            justify=tk.CENTER,
        )
        subtitle_label.pack(pady=(0, 25))

        # Input Card Box (High contrast, clearly visible border and card background)
        card_frame = tk.LabelFrame(
            self.home_frame,
            text=" 📝 Detective Registration ",
            font=("Helvetica", 12, "bold"),
            fg="#facc15",
            bg="#1e293b",
            padx=20,
            pady=20,
            bd=2,
            relief=tk.GROOVE,
        )
        card_frame.pack(pady=15)

        name_prompt = tk.Label(
            card_frame,
            text="Enter Detective Name:",
            font=("Helvetica", 11, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        )
        # Tkinter Checklist: 5. Layout manager - grid() inside card_frame
        name_prompt.grid(row=0, column=0, padx=12, pady=10, sticky=tk.W)

        # Tkinter Checklist: 6. Text and Input widgets - Entry (Crisp white box with dark bold text)
        name_entry = tk.Entry(
            card_frame,
            textvariable=self.player_name_var,
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            fg="#0f172a",
            insertbackground="#0f172a",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=2,
            highlightcolor="#38bdf8",
            width=22,
        )
        name_entry.grid(row=0, column=1, padx=12, pady=10, ipady=4)

        # Tkinter Checklist: 3. Buttons & 7. Event handlers and callbacks (command)
        btn_frame = tk.Frame(self.home_frame, bg="#0f172a")
        btn_frame.pack(pady=25)

        start_btn = tk.Button(
            btn_frame,
            text="▶  Start New Investigation",
            font=("Helvetica", 12, "bold"),
            fg="#065f46",
            bg="#d1fae5",
            highlightbackground="#0f172a",
            padx=20,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.start_game,
        )
        start_btn.pack(pady=6, fill=tk.X)

        load_btn = tk.Button(
            btn_frame,
            text="📂  Load Saved Investigation",
            font=("Helvetica", 11, "bold"),
            fg="#1e40af",
            bg="#dbeafe",
            highlightbackground="#0f172a",
            padx=20,
            pady=6,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.load_game,
        )
        load_btn.pack(pady=6, fill=tk.X)

        exit_btn = tk.Button(
            btn_frame,
            text="✖  Exit Game",
            font=("Helvetica", 10),
            fg="#374151",
            bg="#f3f4f6",
            highlightbackground="#0f172a",
            padx=20,
            pady=4,
            command=self.root.quit,
        )
        exit_btn.pack(pady=6, fill=tk.X)

        db_btn = tk.Button(
            btn_frame,
            text="⚙️  MySQL Database Settings",
            font=("Helvetica", 10, "bold"),
            fg="#7c2d12",
            bg="#ffedd5",
            highlightbackground="#0f172a",
            padx=20,
            pady=4,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.open_db_settings_dialog,
        )
        db_btn.pack(pady=6, fill=tk.X)

        # Database connection indicator
        self.update_home_db_status()
        db_status_label = tk.Label(
            self.home_frame,
            textvariable=self.db_status_var,
            font=("Helvetica", 10),
            fg="#94a3b8",
            bg="#0f172a",
        )
        db_status_label.pack(pady=(12, 0))

    # ========================================================
    # SCREEN 2: PLAY SCREEN
    # ========================================================
    def start_game(self):
        """Validates player name and transitions to the Play Screen."""
        # Python Checklist: 5. if, elif and else
        player_name = self.player_name_var.get().strip()
        if not player_name:
            # Tkinter Checklist: 9. Message boxes
            messagebox.showwarning("Name Required", "Please enter your Detective Name to proceed!")
            return

        self.create_play_screen()

    def create_play_screen(self):
        """Constructs the multi-pane investigation game screen."""
        if self.home_frame:
            self.home_frame.destroy()

        self.play_frame = tk.Frame(self.root, bg="#0f172a", padx=15, pady=15)
        self.play_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- Top Header Bar ----------------
        top_bar = tk.Frame(self.play_frame, bg="#1e293b", padx=14, pady=10, bd=2, relief=tk.GROOVE)
        top_bar.pack(fill=tk.X, pady=(0, 10))

        # Python Checklist: 2. Strings and string formatting (f-strings)
        header_text = f"🕵️ Detective: {self.player_name_var.get()}  |  Chapter {self.level_var.get()}: Midnight Manor"
        self.header_label = tk.Label(
            top_bar,
            text=header_text,
            font=("Helvetica", 13, "bold"),
            fg="#facc15",
            bg="#1e293b",
        )
        self.header_label.pack(side=tk.LEFT)

        self.score_label = tk.Label(
            top_bar,
            text=f"Score: {self.score_var.get()} pts",
            font=("Helvetica", 13, "bold"),
            fg="#4ade80",
            bg="#1e293b",
        )
        self.score_label.pack(side=tk.RIGHT)

        # ---------------- Center Workspace ----------------
        workspace = tk.Frame(self.play_frame, bg="#0f172a")
        workspace.pack(fill=tk.BOTH, expand=True)

        # LEFT COLUMN: Action Panels (Suspects & Clues)
        left_panel = tk.Frame(workspace, bg="#0f172a", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        # Suspects Section Box (Distinct background, border, and gold header)
        suspects_frame = tk.LabelFrame(
            left_panel,
            text=" 👥 Question Suspects ",
            font=("Helvetica", 11, "bold"),
            fg="#facc15",
            bg="#1e293b",
            padx=10,
            pady=10,
            bd=2,
            relief=tk.GROOVE,
        )
        suspects_frame.pack(fill=tk.X, pady=(0, 12))

        # Python Checklist: 6. Loops (Populate suspect buttons dynamically)
        for suspect_title in self.suspects.keys():
            btn = tk.Button(
                suspects_frame,
                text=f"💬 {suspect_title}",
                font=("Helvetica", 10, "bold"),
                fg="#0f172a",
                bg="#f8fafc",
                highlightbackground="#1e293b",
                anchor=tk.W,
                relief=tk.RAISED,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda s=suspect_title: self.question_suspect(s),
            )
            btn.pack(fill=tk.X, pady=4)

        # Clues Section Box (Distinct background, border, and gold header)
        clues_frame = tk.LabelFrame(
            left_panel,
            text=" 🔍 Inspect Evidence ",
            font=("Helvetica", 11, "bold"),
            fg="#facc15",
            bg="#1e293b",
            padx=10,
            pady=10,
            bd=2,
            relief=tk.GROOVE,
        )
        clues_frame.pack(fill=tk.X, pady=(0, 10))

        # Python Checklist: 6. Loops (Populate clue buttons dynamically)
        for clue_name in self.clues.keys():
            btn = tk.Button(
                clues_frame,
                text=f"🔎 {clue_name}",
                font=("Helvetica", 10, "bold"),
                fg="#0f172a",
                bg="#f8fafc",
                highlightbackground="#1e293b",
                anchor=tk.W,
                relief=tk.RAISED,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda c=clue_name: self.inspect_clue(c),
            )
            btn.pack(fill=tk.X, pady=4)

        # RIGHT COLUMN: Case Notebook (Text + Scrollbar Box)
        right_panel = tk.LabelFrame(
            workspace,
            text=" 📜 Case File & Investigation Log ",
            font=("Helvetica", 11, "bold"),
            fg="#facc15",
            bg="#1e293b",
            padx=10,
            pady=10,
            bd=2,
            relief=tk.GROOVE,
        )
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tkinter Checklist: 11. Scrollbar paired with 6. Text widget
        scrollbar = tk.Scrollbar(right_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notebook_text = tk.Text(
            right_panel,
            wrap=tk.WORD,
            bg="#020617",
            fg="#f8fafc",
            font=("Menlo", 11),
            yscrollcommand=scrollbar.set,
            padx=14,
            pady=14,
            relief=tk.SUNKEN,
            bd=1,
            insertbackground="#ffffff",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
        )
        self.notebook_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.notebook_text.yview)

        # Initial briefing message
        briefing = (
            "CASE BRIEFING:\n"
            "==================================================\n"
            "Victim: Lord Harrington\n"
            "Incident: Midnight Emerald stolen from the study safe at 10:00 PM.\n"
            "Goal: Interrogate the 3 suspects, inspect all 4 clues, and name the culprit!\n\n"
            "👉 Click on any Suspect or Clue on the left to begin your investigation.\n"
            "==================================================\n\n"
        )
        self.log_message(briefing)

        # ---------------- Bottom Navigation & Accusation Bar ----------------
        bottom_bar = tk.Frame(self.play_frame, bg="#1e293b", padx=12, pady=10, bd=2, relief=tk.GROOVE)
        bottom_bar.pack(fill=tk.X, pady=(10, 0))

        # Tkinter Checklist: 8. Widget configuration - configure()
        self.status_label = tk.Label(
            bottom_bar,
            textvariable=self.status_var,
            font=("Helvetica", 10, "italic"),
            fg="#94a3b8",
            bg="#1e293b",
        )
        self.status_label.pack(side=tk.LEFT)

        home_btn = tk.Button(
            bottom_bar,
            text="🏠 Menu",
            font=("Helvetica", 10, "bold"),
            fg="#334155",
            bg="#f1f5f9",
            highlightbackground="#1e293b",
            padx=8,
            command=self.return_to_home,
        )
        home_btn.pack(side=tk.RIGHT, padx=3)

        db_btn = tk.Button(
            bottom_bar,
            text="⚙️ DB",
            font=("Helvetica", 10, "bold"),
            fg="#7c2d12",
            bg="#ffedd5",
            highlightbackground="#1e293b",
            padx=8,
            command=self.open_db_settings_dialog,
        )
        db_btn.pack(side=tk.RIGHT, padx=3)

        load_btn = tk.Button(
            bottom_bar,
            text="📂 Load",
            font=("Helvetica", 10, "bold"),
            fg="#15803d",
            bg="#dcfce7",
            highlightbackground="#1e293b",
            padx=8,
            command=self.load_game,
        )
        load_btn.pack(side=tk.RIGHT, padx=3)

        save_btn = tk.Button(
            bottom_bar,
            text="💾 Save (MySQL)",
            font=("Helvetica", 10, "bold"),
            fg="#1e40af",
            bg="#dbeafe",
            highlightbackground="#1e293b",
            padx=10,
            command=self.save_game,
        )
        save_btn.pack(side=tk.RIGHT, padx=3)

        accuse_btn = tk.Button(
            bottom_bar,
            text="⚖️ Make Final Accusation",
            font=("Helvetica", 10, "bold"),
            fg="#991b1b",
            bg="#fee2e2",
            highlightbackground="#1e293b",
            padx=12,
            command=self.open_accusation_dialog,
        )
        accuse_btn.pack(side=tk.RIGHT, padx=6)

    # ========================================================
    # GAMEPLAY LOGIC & ACTIONS
    # Python Checklist: 7. Functions (Reusable actions)
    # ========================================================
    def log_message(self, message: str):
        """Appends formatted text into the scrollable case file notebook."""
        self.notebook_text.insert(tk.END, message)
        self.notebook_text.see(tk.END)

    def question_suspect(self, suspect_title: str):
        """Interrogates a suspect and displays their alibi, motive, and evidence."""
        suspect = self.suspects[suspect_title]

        # Python Checklist: 5. if, elif and else
        if suspect_title not in self.questioned_suspects:
            self.questioned_suspects.append(suspect_title)
            # Award points for thorough investigation
            new_score = self.score_var.get() + 10
            self.score_var.set(new_score)
            self.update_score_display()

        dialogue = (
            f"🗣️ QUESTIONING: {suspect_title}\n"
            f"• Motive: {suspect['motive']}\n"
            f"• Claimed Alibi: \"{suspect['alibi']}\"\n"
            f"• Detective's Observation: {suspect['evidence_found']}\n"
            f"{'-'*50}\n"
        )
        self.log_message(dialogue)

        # Tkinter Checklist: 8. Widget configuration - configure()
        self.status_var.set(f"Interrogated {suspect['name']}. Questioned: {len(self.questioned_suspects)}/3 suspects.")

    def inspect_clue(self, clue_name: str):
        """Examines an environmental clue and logs findings to the notebook."""
        clue = self.clues[clue_name]

        # Python Checklist: 5. if, elif and else
        if clue_name not in self.discovered_clues:
            self.discovered_clues.append(clue_name)
            bonus = clue["bonus"]
            self.score_var.set(self.score_var.get() + bonus)
            self.update_score_display()
            log_header = f"✨ NEW CLUE DISCOVERED: [{clue_name}] (+{bonus} pts)"
        else:
            log_header = f"🔍 RE-EXAMINED: [{clue_name}]"

        log_body = f"{log_header}\n{clue['desc']}\n{'-'*50}\n"
        self.log_message(log_body)
        self.status_var.set(f"Clues discovered: {len(self.discovered_clues)}/4")

    def update_score_display(self):
        """Refreshes the score label widget dynamically."""
        # Tkinter Checklist: 8. Widget configuration
        self.score_label.configure(text=f"Score: {self.score_var.get()} pts")

    def open_accusation_dialog(self):
        """Opens a modal window for submitting the final accusation."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Submit Your Final Accusation")
        dialog.geometry("440x330")
        dialog.configure(bg="#0f172a")
        dialog.transient(self.root)
        dialog.grab_set()

        heading = tk.Label(
            dialog,
            text="Who stole the Midnight Emerald?",
            font=("Helvetica", 13, "bold"),
            fg="#facc15",
            bg="#0f172a",
        )
        heading.pack(pady=(20, 15))

        box_frame = tk.Frame(dialog, bg="#1e293b", padx=15, pady=15, bd=2, relief=tk.GROOVE)
        box_frame.pack(fill=tk.X, padx=25, pady=5)

        # Radio options for each suspect using Loops
        self.selected_suspect_var.set(list(self.suspects.keys())[0])

        for suspect_title in self.suspects.keys():
            rb = tk.Radiobutton(
                box_frame,
                text=f"👉  {suspect_title}",
                variable=self.selected_suspect_var,
                value=suspect_title,
                font=("Helvetica", 11, "bold"),
                fg="#f8fafc",
                bg="#1e293b",
                selectcolor="#0f172a",
                activebackground="#1e293b",
                activeforeground="#facc15",
                anchor=tk.W,
            )
            rb.pack(fill=tk.X, pady=6)

        submit_btn = tk.Button(
            dialog,
            text="⚖️  Confirm Final Verdict",
            font=("Helvetica", 11, "bold"),
            fg="#991b1b",
            bg="#fee2e2",
            highlightbackground="#0f172a",
            padx=15,
            pady=6,
            command=lambda: self.evaluate_accusation(dialog),
        )
        submit_btn.pack(pady=20)

    def evaluate_accusation(self, dialog: tk.Toplevel):
        """Validates the accusation using if, elif, else logic and shows final outcome."""
        chosen = self.selected_suspect_var.get()
        dialog.destroy()

        is_guilty = self.suspects[chosen]["is_guilty"]
        all_clues_found = len(self.discovered_clues) == len(self.clues)

        # Python Checklist: 5. if, elif and else
        if is_guilty and all_clues_found:
            self.score_var.set(self.score_var.get() + 100)
            result_msg = (
                f"🎉 CASE SOLVED WITH DISTINCTION!\n\n"
                f"Detective {self.player_name_var.get()}, you caught {chosen}!\n"
                f"The purple velvet scrap matched her torn glove perfectly, and the muddy footprints proved she crept in from the conservatory.\n\n"
                f"Final Master Detective Score: {self.score_var.get()} pts!"
            )
            # Tkinter Checklist: 9. Message boxes
            messagebox.showinfo("Brilliant Detective Work!", result_msg)
        elif is_guilty and not all_clues_found:
            self.score_var.set(self.score_var.get() + 50)
            result_msg = (
                f"✅ CORRECT ACCUSATION!\n\n"
                f"{chosen} confesses! However, because you didn't gather all 4 clues, some evidence remains circumstantial.\n\n"
                f"Final Score: {self.score_var.get()} pts."
            )
            messagebox.showinfo("Case Closed", result_msg)
        else:
            self.score_var.set(max(0, self.score_var.get() - 50))
            self.update_score_display()
            result_msg = (
                f"❌ WRONGFUL ACCUSATION!\n\n"
                f"{chosen} is innocent! Their alibi holds up under police interrogation.\n"
                f"Penalty applied: -50 pts.\n\n"
                f"Re-examine the clues and the suspects' alibis carefully!"
            )
            messagebox.showerror("Mistake!", result_msg)

    # ========================================================
    # FILE HANDLING: SAVE & LOAD PROGRESS (MySQL & Local Backup)
    # Python Checklist: 9. File handling
    # ========================================================
    def update_home_db_status(self):
        """Checks MySQL connection in the background and updates the home label."""
        ok, msg = self.db.test_connection()
        if ok:
            db_name = self.db.config.get("database", "detective_game")
            user = self.db.config.get("user", "root")
            self.db_status_var.set(f"🟢 MySQL Connected: {user}@{self.db.config.get('host', 'localhost')} (`{db_name}`)")
        else:
            self.db_status_var.set("⚪ MySQL: Not configured (Click 'MySQL Database Settings' above)")

    def open_db_settings_dialog(self):
        """Displays modal to configure MySQL credentials and test the connection."""
        dialog = tk.Toplevel(self.root)
        dialog.title("MySQL Database Settings")
        dialog.geometry("480x420")
        dialog.configure(bg="#0f172a")
        dialog.transient(self.root)
        dialog.grab_set()

        heading = tk.Label(
            dialog,
            text="⚙️ MySQL Connection Settings",
            font=("Helvetica", 14, "bold"),
            fg="#facc15",
            bg="#0f172a",
        )
        heading.pack(pady=(18, 10))

        form_frame = tk.Frame(dialog, bg="#1e293b", padx=20, pady=15, bd=2, relief=tk.GROOVE)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        fields = [
            ("Host:", "host", self.db.config.get("host", "localhost")),
            ("Port:", "port", str(self.db.config.get("port", 3306))),
            ("Username:", "user", self.db.config.get("user", "root")),
            ("Password:", "password", self.db.config.get("password", "")),
            ("Database:", "database", self.db.config.get("database", "detective_game")),
        ]

        entries = {}
        for row_idx, (label_text, key, val) in enumerate(fields):
            lbl = tk.Label(
                form_frame,
                text=label_text,
                font=("Helvetica", 10, "bold"),
                fg="#f8fafc",
                bg="#1e293b",
            )
            lbl.grid(row=row_idx, column=0, sticky=tk.W, pady=6, padx=6)

            is_pwd = key == "password"
            entry = tk.Entry(
                form_frame,
                font=("Helvetica", 11),
                bg="#ffffff",
                fg="#0f172a",
                insertbackground="#0f172a",
                show="*" if is_pwd else "",
                width=24,
            )
            entry.insert(0, val)
            entry.grid(row=row_idx, column=1, sticky=tk.EW, pady=6, padx=6)
            entries[key] = entry

        # Test Connection Action
        def do_test():
            cfg = {
                "host": entries["host"].get().strip(),
                "port": int(entries["port"].get().strip() or 3306),
                "user": entries["user"].get().strip(),
                "password": entries["password"].get(),
                "database": entries["database"].get().strip(),
            }
            ok, err = self.db.test_connection(cfg)
            if ok:
                messagebox.showinfo("Connection Success", "✅ Successfully connected to MySQL server!", parent=dialog)
            else:
                messagebox.showerror("Connection Failed", f"❌ Connection Error:\n{err}", parent=dialog)

        # Save and Apply Action
        def do_save():
            try:
                port_val = int(entries["port"].get().strip() or 3306)
            except ValueError:
                messagebox.showerror("Invalid Input", "Port must be an integer (e.g. 3306).", parent=dialog)
                return

            new_cfg = {
                "host": entries["host"].get().strip(),
                "port": port_val,
                "user": entries["user"].get().strip(),
                "password": entries["password"].get(),
                "database": entries["database"].get().strip(),
            }
            save_db_config(new_cfg)
            self.db.config = new_cfg
            initialized = self.db.init_database()
            self.update_home_db_status()

            if initialized:
                messagebox.showinfo("Saved", "✅ MySQL settings saved and database initialized!", parent=dialog)
                dialog.destroy()
            else:
                ok, err = self.db.test_connection()
                messagebox.showwarning(
                    "Saved with Warning",
                    f"Settings saved, but could not initialize database.\nDetails: {err}",
                    parent=dialog,
                )
                dialog.destroy()

        # Action Buttons
        btn_box = tk.Frame(dialog, bg="#0f172a")
        btn_box.pack(pady=15)

        test_btn = tk.Button(
            btn_box,
            text="🔌 Test Connection",
            font=("Helvetica", 10, "bold"),
            fg="#1e40af",
            bg="#dbeafe",
            highlightbackground="#0f172a",
            padx=12,
            pady=4,
            command=do_test,
        )
        test_btn.pack(side=tk.LEFT, padx=6)

        save_cfg_btn = tk.Button(
            btn_box,
            text="💾 Save & Connect",
            font=("Helvetica", 10, "bold"),
            fg="#065f46",
            bg="#d1fae5",
            highlightbackground="#0f172a",
            padx=12,
            pady=4,
            command=do_save,
        )
        save_cfg_btn.pack(side=tk.LEFT, padx=6)

        cancel_btn = tk.Button(
            btn_box,
            text="Cancel",
            font=("Helvetica", 10),
            fg="#374151",
            bg="#f3f4f6",
            highlightbackground="#0f172a",
            padx=10,
            pady=4,
            command=dialog.destroy,
        )
        cancel_btn.pack(side=tk.LEFT, padx=6)

    def save_game(self):
        """Saves current player progress to MySQL database with local JSON file fallback."""
        player_name = self.player_name_var.get().strip() or "Holmes"
        score = self.score_var.get()
        level = self.level_var.get()

        # Step 1: Save local backup copy
        local_data = {
            "player_name": player_name,
            "score": score,
            "level": level,
            "discovered_clues": self.discovered_clues,
            "questioned_suspects": self.questioned_suspects,
        }
        try:
            with open(self.save_file_path, "w", encoding="utf-8") as f:
                json.dump(local_data, f, indent=4)
        except IOError:
            pass

        # Step 2: Save to MySQL
        success, message = self.db.save_game(
            player_name=player_name,
            score=score,
            level=level,
            discovered_clues=self.discovered_clues,
            questioned_suspects=self.questioned_suspects,
        )

        if success:
            self.status_var.set(f"Saved to MySQL ({self.db.config['database']}.game_saves)")
            messagebox.showinfo(
                "Game Saved",
                f"✅ Progress for Detective '{player_name}' saved to MySQL!\n\n"
                f"Database: {self.db.config['database']}\n"
                f"Table: game_saves\n"
                f"(Local backup file '{os.path.basename(self.save_file_path)}' also updated)",
            )
        else:
            self.status_var.set("MySQL save failed (saved to local backup).")
            open_settings = messagebox.askyesno(
                "MySQL Save Error",
                f"Could not save to MySQL:\n{message}\n\n"
                f"✅ Don't worry! Your game was safely saved to local file: {os.path.basename(self.save_file_path)}.\n\n"
                f"Would you like to open MySQL Settings now to configure or check your credentials?",
            )
            if open_settings:
                self.open_db_settings_dialog()

    def load_game(self):
        """Loads player progress from MySQL or local JSON backup."""
        saves = self.db.get_all_saves()
        if saves:
            self.open_load_dialog(saves)
        else:
            self.load_from_local_file()

    def open_load_dialog(self, saves: list):
        """Displays saved detective records from MySQL allowing player to select one."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Saved Detective")
        dialog.geometry("520x400")
        dialog.configure(bg="#0f172a")
        dialog.transient(self.root)
        dialog.grab_set()

        heading = tk.Label(
            dialog,
            text="📂 Saved Detectives in MySQL",
            font=("Helvetica", 13, "bold"),
            fg="#facc15",
            bg="#0f172a",
        )
        heading.pack(pady=(15, 8))

        sub = tk.Label(
            dialog,
            text="Select a case file to resume your investigation:",
            font=("Helvetica", 10),
            fg="#94a3b8",
            bg="#0f172a",
        )
        sub.pack(pady=(0, 10))

        list_frame = tk.Frame(dialog, bg="#1e293b", bd=2, relief=tk.GROOVE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            list_frame,
            font=("Menlo", 10),
            bg="#020617",
            fg="#f8fafc",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            yscrollcommand=scrollbar.set,
            height=8,
        )
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate listbox with saves
        for s in saves:
            line = f"🕵️ {s['player_name']:<16} | Score: {s['score']:<4} | Ch.{s['level']} | {str(s.get('saved_at', ''))[:16]}"
            listbox.insert(tk.END, line)
        listbox.select_set(0)

        def do_load_selected():
            sel = listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            selected_name = saves[idx]["player_name"]
            dialog.destroy()
            ok, data, err = self.db.load_game(selected_name)
            if ok and data:
                self.apply_loaded_state(data, source="MySQL")
            else:
                messagebox.showerror("Load Failed", f"Failed to load record from MySQL:\n{err}")

        btn_box = tk.Frame(dialog, bg="#0f172a")
        btn_box.pack(pady=15)

        load_btn = tk.Button(
            btn_box,
            text="▶ Load Selected Detective",
            font=("Helvetica", 10, "bold"),
            fg="#065f46",
            bg="#d1fae5",
            highlightbackground="#0f172a",
            padx=12,
            pady=5,
            command=do_load_selected,
        )
        load_btn.pack(side=tk.LEFT, padx=6)

        local_btn = tk.Button(
            btn_box,
            text="📄 Load from Local File",
            font=("Helvetica", 10),
            fg="#1e40af",
            bg="#dbeafe",
            highlightbackground="#0f172a",
            padx=10,
            pady=5,
            command=lambda: [dialog.destroy(), self.load_from_local_file()],
        )
        local_btn.pack(side=tk.LEFT, padx=6)

        cancel_btn = tk.Button(
            btn_box,
            text="Cancel",
            font=("Helvetica", 10),
            fg="#374151",
            bg="#f3f4f6",
            highlightbackground="#0f172a",
            padx=10,
            pady=5,
            command=dialog.destroy,
        )
        cancel_btn.pack(side=tk.LEFT, padx=6)

    def apply_loaded_state(self, game_data: dict, source: str = "MySQL"):
        """Applies loaded dictionary state to game variables and rebuilds screen."""
        self.player_name_var.set(game_data.get("player_name", "Holmes"))
        self.score_var.set(game_data.get("score", 100))
        self.level_var.set(game_data.get("level", 1))
        self.discovered_clues = game_data.get("discovered_clues", [])
        self.questioned_suspects = game_data.get("questioned_suspects", [])

        self.create_play_screen()

        restore_msg = (
            f"📂 RESTORED SAVE FILE VIA {source.upper()}:\n"
            f"• Detective: {self.player_name_var.get()}\n"
            f"• Current Score: {self.score_var.get()} pts\n"
            f"• Clues Found: {len(self.discovered_clues)}/4\n"
            f"• Suspects Interrogated: {len(self.questioned_suspects)}/3\n"
            f"{'='*50}\n\n"
        )
        self.log_message(restore_msg)
        messagebox.showinfo("Game Loaded", f"Successfully loaded investigation for Detective {self.player_name_var.get()} ({source})!")

    def load_from_local_file(self):
        """Loads player progress from the local JSON save file."""
        if not os.path.exists(self.save_file_path):
            messagebox.showinfo(
                "No Saves Found",
                "No saved records found in MySQL or local file.\nStart a new investigation and click 'Save (MySQL)'!",
            )
            return

        try:
            with open(self.save_file_path, "r", encoding="utf-8") as f:
                game_data = json.load(f)
            self.apply_loaded_state(game_data, source="Local File")
        except (IOError, json.JSONDecodeError) as e:
            messagebox.showerror("Load Error", f"Failed to read local save file: {e}")

    def return_to_home(self):
        """Confirms and returns to the home screen."""
        confirm = messagebox.askyesno("Return to Home", "Return to main menu? Make sure to save your game first!")
        if confirm:
            if self.play_frame:
                self.play_frame.destroy()
            self.create_home_screen()


# ----------------------------------------------------
# Tkinter Checklist: 12. The event loop - mainloop()
# ----------------------------------------------------
def main():
    root = tk.Tk()
    app = DetectiveGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
