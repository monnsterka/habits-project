import sqlite3
from datetime import date, datetime, timedelta

#DATA

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {path}")
        self.create_table()

    def create_table(self):
        # HABITS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_date TEXT
            )
        """)

        # RECORDS TABLE (tracking done days)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT,
                completed_at TEXT,
                UNIQUE(habit_id, date)
            )
        """)

        # migrate existing databases that predate these columns
        try:
            self.cursor.execute("ALTER TABLE habits ADD COLUMN created_date TEXT")
        except Exception:
            pass

        try:
            self.cursor.execute("ALTER TABLE records ADD COLUMN completed_at TEXT")
        except Exception:
            pass

        self.conn.commit()

    def add_habit(self, name, periodicity):
        created_date = date.today().isoformat()
        self.cursor.execute(
            "INSERT INTO habits (name, periodicity, created_date) VALUES (?, ?, ?)",
            (name, periodicity, created_date)
        )
        self.conn.commit()

    def get_habits(self):
        self.cursor.execute("SELECT id, name, periodicity, created_date FROM habits ORDER BY id")
        return self.cursor.fetchall()

    def delete_habit(self, habit_id):
        self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()

    def update_habit(self, habit_id, new_name):
        self.cursor.execute(
            "UPDATE habits SET name = ? WHERE id = ?",
            (new_name, habit_id)
        )
        self.conn.commit()

    def mark_done(self, habit_id, today):
        completed_at = datetime.now().isoformat(timespec="seconds")
        self.cursor.execute(
            "INSERT OR IGNORE INTO records (habit_id, date, completed_at) VALUES (?, ?, ?)",
            (habit_id, today, completed_at)
        )
        self.conn.commit()

    def is_done_today(self, habit_id, today):
        self.cursor.execute(
            "SELECT 1 FROM records WHERE habit_id = ? AND date = ?",
            (habit_id, today)
        )
        return self.cursor.fetchone() is not None

    def get_streak(self, habit_id):
        self.cursor.execute("SELECT periodicity FROM habits WHERE id = ?", (habit_id,))
        row = self.cursor.fetchone()
        if not row:
            return 0
        periodicity = row[0].strip().lower()

        self.cursor.execute(
            "SELECT date FROM records WHERE habit_id = ? ORDER BY date DESC",
            (habit_id,)
        )
        rows = self.cursor.fetchall()

        if not rows:
            return 0

        if periodicity == "daily":
            streak = 0
            today = date.today()
            yesterday = today - timedelta(days=1)

            for i, (d,) in enumerate(rows):
                record_date = date.fromisoformat(d)

                if i == 0:
                    if record_date != today and record_date != yesterday:
                        return 0

                if i > 0:
                    prev_date = date.fromisoformat(rows[i - 1][0])
                    if (prev_date - record_date).days != 1:
                        break

                streak += 1

            return streak

        elif periodicity == "weekly":
            # collect unique (year, week) pairs, newest first
            weeks = sorted(
                set(date.fromisoformat(d).isocalendar()[:2] for (d,) in rows),
                reverse=True
            )

            today = date.today()
            current_week = today.isocalendar()[:2]
            prev_week = (today - timedelta(weeks=1)).isocalendar()[:2]

            # streak is broken if the most recent week isn't this week or last week
            if weeks[0] != current_week and weeks[0] != prev_week:
                return 0

            streak = 0
            for i, week in enumerate(weeks):
                if i == 0:
                    streak += 1
                    continue

                # compare the Monday of each week to check they are exactly 7 days apart
                prev_monday = date.fromisocalendar(weeks[i - 1][0], weeks[i - 1][1], 1)
                curr_monday = date.fromisocalendar(week[0], week[1], 1)

                if (prev_monday - curr_monday).days != 7:
                    break

                streak += 1

            return streak

        return 0

    def seed_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM habits")
        if self.cursor.fetchone()[0] > 0:
            return

        today = date.today()
        created = (today - timedelta(days=28)).isoformat()

        habits = [
            ("Drink water", "daily"),
            ("Exercise", "daily"),
            ("Read a book", "daily"),
            ("Weekly review", "weekly"),
            ("Clean the house", "weekly"),
        ]

        habit_ids = []
        for name, periodicity in habits:
            self.cursor.execute(
                "INSERT INTO habits (name, periodicity, created_date) VALUES (?, ?, ?)",
                (name, periodicity, created)
            )
            habit_ids.append(self.cursor.lastrowid)

        def add_record(habit_id, d):
            completed_at = f"{d.isoformat()}T08:00:00"
            self.cursor.execute(
                "INSERT OR IGNORE INTO records (habit_id, date, completed_at) VALUES (?, ?, ?)",
                (habit_id, d.isoformat(), completed_at)
            )

        # Drink water — completed every day for 4 weeks, two small gaps
        for i in range(28):
            if i not in (10, 20):
                add_record(habit_ids[0], today - timedelta(days=i))

        # Exercise — 7-day current streak, scattered completions before that
        for i in range(7):
            add_record(habit_ids[1], today - timedelta(days=i))
        for i in range(10, 28, 2):
            add_record(habit_ids[1], today - timedelta(days=i))

        # Read a book — broken streak (last done 5 days ago)
        for i in range(5, 28):
            if i % 3 != 0:
                add_record(habit_ids[2], today - timedelta(days=i))

        # Weekly review — completed once every week for 4 weeks (full streak)
        for week in range(4):
            add_record(habit_ids[3], today - timedelta(weeks=week))

        # Clean the house — missed 2 weeks ago (broken streak)
        add_record(habit_ids[4], today)
        add_record(habit_ids[4], today - timedelta(weeks=1))
        add_record(habit_ids[4], today - timedelta(weeks=3))

        self.conn.commit()
        print("Sample data loaded.")

    def close(self):
        self.conn.close()
        print("Database closed")