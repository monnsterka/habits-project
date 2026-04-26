import argparse
import os
import sqlite3
from datetime import date, timedelta


class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {path}")

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT,
                UNIQUE(habit_id, date)
            )
        """)
        
        self.conn.commit()

    def add_habit(self, name):
        self.cursor.execute(
            "INSERT INTO habits (name) VALUES (?)",
            (name,) 
        )
        self.conn.commit()

    def get_habits(self):
        self.cursor.execute("SELECT id, name FROM habits")
        return self.cursor.fetchall()
    
    def delete_habit(self, habit_id):
        self.cursor.execute(
            "DELETE FROM habits WHERE id = ? ",
            (habit_id,)
        )
        self.conn.commit()

    def update_habit(self, habit_id, new_name):
        self.cursor.execute(
            "UPDATE habits SET name = ? WHERE id = ?",
            (new_name, habit_id)
        )
        self.conn.commit()

    
    def mark_done(self,habit_id, today):
        try:
            self.cursor.execute(
                "INSERT INTO records (habit_id, date) VALUES (?, ?)",
                (habit_id, today)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Already marked as done today")

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
        yesterday = today - timedelta(days = 1)

        for i, (d,) in enumerate(rows):
            record_date = date.fromisoformat(d)

            # first day needs to be today or yesterday 
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


# CLI

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data.db")
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args()


def menu():
    print("\n--- MENU ---")
    print("1 - create habit")
    print("2 - show habits")
    print("3 - delete habit")
    print("4 - update habit")
    print("5 - mark habit as done today")
    print("0 - Quit")

    return input("Choose option: ")


def add_habit(db):
    name = input("Write name of the habit: ")
    db.add_habit(name)
    print(f"Habit '{name}' added")


def show_habits(db):
    today = date.today().isoformat()
    habits = db.get_habits()

    if not habits:
        print("No habits")
    else:
        for h in habits:
            done = db.is_done_today(h[0], today)
            streak = db.get_streak(h[0])
            status = "✔" if done else "✘"

            print(f"{h[0]} - {h[1]} [{status}] 🔥{streak}")

def delete_habit(db):
    try:
        habit_id = int(input("Enter habit ID to delete:  "))

        habits = db.get_habits()
        ids = [h[0] for h in habits]

        if habit_id not in ids:
            print("Habit does not exist")
            return

        db.delete_habit(habit_id)
        print("Habit deleted")

    except ValueError:
        print("Invalid ID")

def update_habit(db):
    try:
        habit_id = int(input("Enter habit ID to update:  "))
        new_name = input("Enter new name:  ")

        habits = db.get_habits()
        ids = [h[0] for h in habits]

        if habit_id not in ids:
            print("Habit does not exist")
            return

        db.update_habit(habit_id, new_name)
        print("Habit updated")

    except ValueError:
        print("Invalid input")

def mark_done(db):
    try:
        habit_id = int(input("Enter habit ID: "))
        today = date.today().isoformat()

        habits = db.get_habits()
        ids = [h[0] for h in habits]

        if habit_id not in ids:
            print("Habit does not exist")
            return

        db.mark_done(habit_id, today)
        print("Marked as done")

    except ValueError:
        print("Invalid ID")


# MAIN

def main():
    args = parse_args()

    if args.reset and os.path.exists(args.db):
        os.remove(args.db)
        print("Database reset")

    db = Database(args.db)

    while True:
        choice = menu()

        if choice == "1":
            add_habit(db)

        elif choice == "2":
            show_habits(db)

        elif choice == "3":
            delete_habit(db)

        elif choice == "4":
            update_habit(db)

        elif choice == "5":
            mark_done(db)

        elif choice == "0":
            print("Ending the application")
            break

        else:
            print("Incorrect choice")

    db.close()


if __name__ == "__main__":
    main()