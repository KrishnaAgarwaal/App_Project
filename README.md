# Midnight Manor Mystery 🕵️

A text-based detective investigation desktop game built with Python and Tkinter.

## 📖 Story Overview

The famous **Midnight Emerald** has vanished from Lord Harrington's private study safe at 10:00 PM during a sudden manor blackout. As the lead detective, you must:
- Interrogate three suspects with conflicting alibis and hidden motives.
- Search for physical clues and forensic evidence across the crime scene.
- Maintain your investigation notes in real time.
- Deduce the culprit and deliver your final verdict!

## ✨ Features

- **Home Screen & Play Screen**: Smooth screen navigation with detective name input and saved case loading.
- **Interactive Suspect Interrogations**: Question suspects to reveal their motives, alibis, and inconsistencies.
- **Evidence Inspection**: Discover hidden clues that award score points and build your case.
- **Scrollable Detective Notebook**: Integrated case file and real-time investigation log.
- **High-Contrast Modern UI**: Optimized color scheme and borders for clear readability across operating systems (macOS, Windows, Linux).
- **Persistent Game Saves (MySQL & JSON)**: Save and load progress directly to/from a **MySQL** database (`game_saves` table) with multi-profile support and automatic local backup (`savegame.json`).
- **Database Settings Manager**: In-game GUI dialog to test connection, configure MySQL host, user, and password on the fly.
- **Accusation System**: Dynamic grading based on clues found, suspect evaluations, and deductive accuracy.

## 🚀 How to Run

### Prerequisites
- Python 3.8+ (includes Tkinter by default on most platforms)
- MySQL Server (optional but recommended for database saves)

### Installation
Install the database driver:
```bash
pip install -r requirements.txt
```

### Launching the Game
```bash
python3 main.py
```

### 🗄️ MySQL Database Setup
The game automatically creates the database (`detective_game`) and table (`game_saves`) upon your first save or connection test.

You can configure your MySQL credentials directly inside the game:
1. Click **⚙️ MySQL Database Settings** on the home screen.
2. Enter your MySQL username and password.
3. Click **🔌 Test Connection** and then **💾 Save & Connect**.
