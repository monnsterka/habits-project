import argparse
import os
import json


class Database:
    def __init__(self, path):
        self.path = path
        print(f"Database connected to DB: {path}")

    def close(self):
        print("Database is closed")


class Habit:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        return Habit(data["name"])


#Json storage

def save_habits(habits, file):
    data = [h.to_dict() for h in habits]

    with open(file, "w") as f:
        json.dump(data, f)


def load_habits(file):
    if not os.path.exists(file):
        return []

    with open(file, "r") as f:
        data = json.load(f)

    return [Habit.from_dict(d) for d in data]


# CLI

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--db", default="data.json")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--seed", action="store_true")

    return parser.parse_args()


def menu():
    print("\n--- MENU ---")
    print("1 - create habit")
    print("2 - show habits")
    print("0 - Quit")

    return input("Choose option: ")


def add_habit(habits):
    name = input("Write name of the habit: ")
    habits.append(Habit(name))
    print(f"Habit '{name}' added")


def show_habits(habits):
    if not habits:
        print("No habits")
    else:
        for h in habits:
            print("-", h.name)


# Main

def main():
    args = parse_args()

    # reset database file
    if args.reset and os.path.exists(args.db):
        os.remove(args.db)
        print("DB removed")

    db = Database(args.db)

    # load existing habits
    habits = load_habits(args.db)

    if args.seed:
        print("Loading testing data...")
        if not habits:
            habits.append(Habit("Drink water"))
            habits.append(Habit("Exercise"))
            habits.append(Habit("Read"))
            habits.append(Habit("Sleep 8h"))
            save_habits(habits, args.db)

    # application loop
    while True:
        choice = menu()

        if choice == "1":
            add_habit(habits)
            save_habits(habits, args.db)

        elif choice == "2":
            show_habits(habits)

        elif choice == "0":
            print("Ending the application")
            break

        else:
            print("Incorrect choice")

    db.close()


if __name__ == "__main__":
    main()