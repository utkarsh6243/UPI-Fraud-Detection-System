import sqlite3

DATABASE = "transactions.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # ---------------- USERS ---------------- #

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ---------------- TRANSACTIONS ---------------- #

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS transactions(

        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

        amount REAL,

        old_balance REAL,

        new_balance REAL,

        upi_id TEXT,

        sender_bank TEXT,

        receiver_bank TEXT,

        location TEXT,

        device TEXT,

        transaction_type TEXT,

        status TEXT,

        fraud_probability REAL,

        prediction TEXT,

        remarks TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ---------------- LOGIN HISTORY ---------------- #

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS login_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        ip_address TEXT,

        status TEXT

    )

    """)

    # ---------------- FRAUD LOGS ---------------- #

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS fraud_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        transaction_id INTEGER,

        fraud_probability REAL,

        reason TEXT,

        action_taken TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ---------------- AI REPORTS ---------------- #

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS ai_reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        total_transactions INTEGER,

        fraud_transactions INTEGER,

        model_accuracy REAL,

        average_probability REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")