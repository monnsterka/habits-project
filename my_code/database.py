import sqlite3
from datetime import date, timedelta

#DATA

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {path}")
        self.create_table()

    def create_table(self):
         # HABITS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL
            )
        """)

        # RECORDS TABLE (tracking done days)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT,
                UNIQUE(habit_id, date)
            )
        """)

        self.conn.commit()

    def add_habit(self, name, periodicity):
        self.cursor.execute(
            "INSERT INTO habits (name, periodicity) VALUES (?, ?)",
            (name, periodicity)
        )
        self.conn.commit()

    def get_habits(self):
        self.cursor.execute("SELECT id, name, periodicity FROM habits ORDER BY id")
        return self.cursor.fetchall()

    def delete_habit(self, habit_id):
        self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()

    def update_habit(self, habit_id, new_name):
        self.cursor.execute(
            "UPDATE habits SET name = ? WHERE id = ?",
            (new_name, habit_id)
        )
        self.conn.commit()

    def mark_done(self, habit_id, today):
        self.cursor.execute(
             "INSERT OR IGNORE INTO records (habit_id, date) VALUES (?, ?)",
            (habit_id, today)
        )
        self.conn.commit()

    def is_done_today(self, habit_id, today):
        self.cursor.execute(
            "SELECT 1 FROM records WHERE habit_id = ? AND date = ?",
            (habit_id, today)
        )
        return self.cursor.fetchone() is not None

    def get_streak(self, habit_id):
        self.cursor.execute(
            "SELECT date FROM records WHERE habit_id = ? ORDER BY date DESC",
            (habit_id,)
        )
        rows = self.cursor.fetchall()

        if not rows:
            return 0

        streak = 0
        today = date.today()
        yesterday = today - timedelta(days=1)

        for i, (d,) in enumerate(rows):
            record_date = date.fromisoformat(d)

            if i == 0:
                if record_date != today and record_date != yesterday:
                    return 0

            if i > 0:
                prev_date = date.fromisoformat(rows[i - 1][0])
                if (prev_date - record_date).days != 1:
                    break

            streak += 1

        return streak

    def close(self):
        self.conn.close()
        print("Database closed")