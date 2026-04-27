#CALCULATIONS
def get_all_habits(db):
    return db.get_habits()

def get_habits_by_periodicity(habits, periodicity):
    return list(filter(lambda h: h[2] == periodicity, habits))


def get_longest_streak_all(db):
    habits = db.get_habits()

    if not habits:
        return 0

    streaks = list(map(lambda h: db.get_streak(h[0]), habits))
    return max(streaks)

def get_longest_streak_for_habit(db, habit_id):
    return db.get_streak(habit_id)