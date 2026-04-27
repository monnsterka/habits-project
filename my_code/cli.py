from datetime import date
from analytics import ( get_all_habits, get_habits_by_periodicity, get_longest_streak_all, get_longest_streak_for_habit )
#COMMUNICATION WITH USER 

def get_habit_by_index(db, index):
    habits = db.get_habits()

    if index < 1 or index > len(habits):
        return None
    
    return habits[index - 1]


def menu():
    print("\n--- MENU ---")
    print("1 - create habit")
    print("2 - show habits")
    print("3 - delete habit")
    print("4 - update habit")
    print("5 - mark habit as done today")
    print("6 - analytics")
    print("0 - Quit")

    return input("Choose option: ")

def analytics_menu():
    print("\n--- ANALYTICS ---")
    print("1 - show all habits")
    print("2 - filter by periodicity")
    print("3 - longest streak (all)")
    print("4 - longest streak (one habit)")
    print("0 - back")

    return input("Choose option: ")


def add_habit(db):
    name = input("Habit name: ")

    while True:
        periodicity = input("Periodicity (daily/weekly): ").strip().lower()
        if periodicity in ("daily", "weekly"):
            break
        print("Invalid input. Please type 'daily' or 'weekly'.")

    db.add_habit(name, periodicity)
    print(f"Habit '{name}' added")


def show_habits(db):
    today = date.today().isoformat()
    habits = db.get_habits()

    if not habits:
        print("No habits")
        return

    for i, h in enumerate(habits, start=1):
        done = db.is_done_today(h[0], today)
        streak = db.get_streak(h[0])
        status = "✔" if done else "✘"

        print(f"{i} - {h[1]} ({h[2]}) [{status}] 🔥{streak}")



def delete_habit(db):
    try:
        index = int(input("Choose habit number to delete: "))
        habit = get_habit_by_index(db, index)

        if not habit:
            print("Invalid choice")
            return

        db.delete_habit(habit[0])
        print("Habit deleted")

    except ValueError:
        print("Invalid input")


def update_habit(db):
    try:
        index = int(input("Choose habit number to update: "))
        new_name = input("Enter new name: ")

        habit = get_habit_by_index(db, index)
        if not habit:
            print("Invalid choice")
            return

        db.update_habit(habit[0], new_name)
        print("Habit updated")

    except ValueError:
        print("Invalid input")


def mark_done(db):
    try:
        index = int(input("Choose habit number: "))
        today = date.today().isoformat()

        habit = get_habit_by_index(db, index)
        if not habit:
            print("Invalid choice")
            return

        db.mark_done(habit[0], today)
        print("Marked as done")

    except ValueError:
        print("Invalid input")

def run_analytics(db):
    while True:
        choice = analytics_menu()

        if choice == "1":
            habits = get_all_habits(db)
            for i, h in enumerate(habits, start=1):
                print(f"{i} - {h[1]} ({h[2]})")

        elif choice == "2":
            p = input("periodicity: ")
            habits = get_all_habits(db)
            result = get_habits_by_periodicity(habits, p)

            if not result:
                print("No habits found with that periodicity")
            else:
                for i, h in enumerate(result, start=1):
                    streak = db.get_streak(h[0])
                    print(f"{i} - {h[1]} ({h[2]}) 🔥{streak}")

        elif choice == "3":
            results = get_longest_streak_all(db)
            for r in results:
                print(f"{r[1]} → 🔥 {r[3]}")

        elif choice == "4":
            try:
                index = int(input("Habit index: "))
                habit = get_habit_by_index(db, index)

                if habit:
                    streak = get_longest_streak_for_habit(db, habit[0])
                    print(f"{habit[1]} → 🔥 {streak}")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid input")

        elif choice == "0":
            break

        else:
            print("Incorrect choice")