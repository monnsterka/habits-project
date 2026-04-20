import argparse
import os

class Database:
    def __init__(self, path):
        self.path = path
        print("Database connected to DB: {path}")

    def close(self):
            print ("Database is closed")

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument ("--db", default= "data.db")
    parser.add_argument ("--reset", action="store_true")
    parser.add_argument ("--seed",action="store_true")

    return parser.parse_args()

def menu():
     print("\n--- MENU ---")
     print("1 - create habit")
     print("2 - show habits")
     print("0 - Quit")

     return input("Choose option: ")

def add_habit(habits):
    name = input ("Write name of the habit: ")
    habits.append(name)
    print (f"Habit '{name}' added")

def show_habits(habits):
    if not habits:
        print("No habits")
    else:
        for n in habits:
            print("-", n)

def main():
    args = parse_args()

    #reset database
    if args.reset and os.path.exists(args.db):
        os.remove(args.db)
        print ("DB removed")

    #create database
    db = Database(args.db)

    #seed data
    if args.seed:
        print ("Loading testing data...")

    habits = []

    #Aplication Start 
    while True:
        choice = menu()

        if choice == "1":
            add_habit(habits)
        elif choice == "2":
            show_habits(habits)
        elif choice == "0":
            print("Ending the application")
            break
        else:
            print("Incorrect choice")


    #Application quit
    db.close()

if __name__ == "__main__":
    main()