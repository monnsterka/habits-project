import argparse
import os

from database import Database
from cli import menu, add_habit, show_habits, delete_habit, update_habit, mark_done, run_analytics

#CONNECTING EVERYTHING AND RUNNING THE MAIN PROGRAM


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data.db")
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args()


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

        elif choice == "6":
            run_analytics(db)

        elif choice == "0":
            print("Ending the application 👋1")
            break

        else:
            print("Incorrect choice")

    db.close()


if __name__ == "__main__":
    main()