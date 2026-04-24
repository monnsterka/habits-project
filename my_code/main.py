import argparse
import os
import sqlite3


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
    print("0 - Quit")
    return input("Choose option: ")


def add_habit(db):
    name = input("Write name of the habit: ")
    db.add_habit(name)
    print(f"Habit '{name}' added")


def show_habits(db):
    habits = db.get_habits()

    if not habits:
        print("No habits")
    else:
        for h in habits:
            print(f"{h[0]} - {h[1]}")

def delete_habit(db):
    try:
        habit_id = int(input("Enter habit ID to delete:  "))
        db.delete_habit(habit_id)
        print("Habit deleted")
    except ValueError:
        print("Habit deleted")


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

        elif choice == "0":
            print("Ending the application")
            break

        else:
            print("Incorrect choice")

    db.close()


if __name__ == "__main__":
    main()