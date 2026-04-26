from datetime import date

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
        for i, h in enumerate(habits, start=1):
            done = db.is_done_today(h[0], today)
            streak = db.get_streak(h[0])
            status = "✔" if done else "✘"

            print(f"{i} - {h[1]} [{status}] 🔥{streak}")


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