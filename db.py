"""
Database Manager for Midnight Manor Mystery
Handles MySQL database connection, schema setup, saving, and loading.
"""

import json
import os
from typing import Any, Dict, List, Optional
import mysql.connector
from mysql.connector import Error

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "db_config.json")

DEFAULT_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "detective_game",
}


def load_db_config() -> Dict[str, Any]:
    """Loads database connection configuration from db_config.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except (IOError, json.JSONDecodeError):
            pass
    return DEFAULT_CONFIG.copy()


def save_db_config(config: Dict[str, Any]) -> None:
    """Saves database configuration to db_config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


class DatabaseManager:
    def __init__(self):
        self.config = load_db_config()

    def get_server_connection(self):
        """Connects to MySQL server (without selecting specific DB)."""
        return mysql.connector.connect(
            host=self.config["host"],
            port=int(self.config["port"]),
            user=self.config["user"],
            password=self.config["password"],
            connect_timeout=5,
        )

    def get_db_connection(self):
        """Connects to the game database."""
        return mysql.connector.connect(
            host=self.config["host"],
            port=int(self.config["port"]),
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            connect_timeout=5,
        )

    def init_database(self) -> bool:
        """
        Creates the database and tables if they do not exist.
        Returns True if successful, False otherwise.
        """
        try:
            # Step 1: Connect to server and create database if missing
            conn = self.get_server_connection()
            cursor = conn.cursor()
            db_name = self.config["database"]
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4;")
            cursor.close()
            conn.close()

            # Step 2: Connect to database and create save table
            db_conn = self.get_db_connection()
            db_cursor = db_conn.cursor()
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS game_saves (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(100) NOT NULL UNIQUE,
                score INT NOT NULL DEFAULT 100,
                level INT NOT NULL DEFAULT 1,
                discovered_clues TEXT,
                questioned_suspects TEXT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            db_cursor.execute(create_table_sql)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            return True
        except Error:
            return False

    def test_connection(self, temp_config: Optional[Dict[str, Any]] = None) -> tuple[bool, str]:
        """Tests the MySQL connection with given or current configuration."""
        cfg = temp_config or self.config
        try:
            conn = mysql.connector.connect(
                host=cfg["host"],
                port=int(cfg["port"]),
                user=cfg["user"],
                password=cfg["password"],
                connect_timeout=5,
            )
            if conn.is_connected():
                conn.close()
                return True, "Successfully connected to MySQL!"
            return False, "Unable to establish connection."
        except Error as e:
            return False, str(e)

    def save_game(
        self,
        player_name: str,
        score: int,
        level: int,
        discovered_clues: List[str],
        questioned_suspects: List[str],
    ) -> tuple[bool, str]:
        """Saves or updates a player's game progress in MySQL."""
        if not self.init_database():
            return False, "Failed to initialize or connect to MySQL database."

        sql = """
        INSERT INTO game_saves (player_name, score, level, discovered_clues, questioned_suspects)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            score = VALUES(score),
            level = VALUES(level),
            discovered_clues = VALUES(discovered_clues),
            questioned_suspects = VALUES(questioned_suspects);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    player_name,
                    score,
                    level,
                    json.dumps(discovered_clues),
                    json.dumps(questioned_suspects),
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, f"Game progress for '{player_name}' saved to MySQL!"
        except Error as e:
            return False, f"MySQL Save Error: {e}"

    def load_game(self, player_name: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
        """Loads game progress for a specific player from MySQL."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT player_name, score, level, discovered_clues, questioned_suspects, saved_at "
                "FROM game_saves WHERE player_name = %s LIMIT 1",
                (player_name,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if not row:
                return False, None, f"No save record found for detective '{player_name}'."

            data = {
                "player_name": row["player_name"],
                "score": int(row["score"]),
                "level": int(row["level"]),
                "discovered_clues": json.loads(row["discovered_clues"]) if row["discovered_clues"] else [],
                "questioned_suspects": json.loads(row["questioned_suspects"]) if row["questioned_suspects"] else [],
                "saved_at": str(row["saved_at"]),
            }
            return True, data, "Loaded successfully!"
        except Error as e:
            return False, None, f"MySQL Load Error: {e}"

    def get_all_saves(self) -> List[Dict[str, Any]]:
        """Retrieves list of all saved detectives from MySQL."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT player_name, score, level, saved_at FROM game_saves ORDER BY saved_at DESC"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error:
            return []
