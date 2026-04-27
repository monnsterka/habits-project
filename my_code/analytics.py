#CALCULATIONS
def get_all_habits(db):
    return db.get_habits()

def get_habits_by_periodicity(habits, periodicity):
    return [
        h for h in habits
        if h[2].strip().lower() == periodicity.strip().lower()
    ]


def get_longest_streak_all(db):
    habits = db.get_habits()

    result = []
    for h in habits:
        streak = db.get_streak(h[0])
        result.append((h[0], h[1], h[2], streak))

    return sorted(result, key=lambda x: x[3], reverse=True)

def get_longest_streak_for_habit(db, habit_id):
    return db.get_streak(habit_id)