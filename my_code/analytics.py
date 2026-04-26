#CALCULATIONS
def get_all_habits(db):
    return db.get_habits()


def get_longest_streak_all(db):
    habits = db.get_habits()
    if not habits:
        return 0

    streaks = [db.get_streak(h[0]) for h in habits]
    return max(streaks)