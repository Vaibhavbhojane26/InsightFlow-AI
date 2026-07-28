import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "database.db"
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# CREATE ALL TABLES
# ==========================================

def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================
    # USERS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        mobile TEXT,

        password_hash TEXT NOT NULL,

        role TEXT DEFAULT 'user',

        status TEXT DEFAULT 'active',

        profile_photo TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        last_login TIMESTAMP

    )

    """)

    # ==========================
    # LOGIN HISTORY
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS login_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        login_time TIMESTAMP,

        logout_time TIMESTAMP,

        ip_address TEXT,

        device TEXT,

        status TEXT,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    # ==========================
    # ACTIVITY LOGS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS activity_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        activity TEXT,

        activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    # ==========================
    # PROJECTS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS projects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        project_name TEXT,

        description TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)


        # ==========================
    # UPLOADED FILES
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS uploaded_files(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    project_id INTEGER,

    file_name TEXT,

    file_path TEXT,

    file_type TEXT,

    file_size REAL,

    total_rows INTEGER,

    total_columns INTEGER,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(project_id)
    REFERENCES projects(id)

)

    """)

    # ==========================
    # REPORTS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        report_name TEXT,

        report_type TEXT,

        report_path TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(project_id)
        REFERENCES projects(id)

    )

    """)

    # ==========================
    # AI HISTORY
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS ai_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        prompt TEXT,

        response TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(project_id)
        REFERENCES projects(id)

    )

    """)

    # ==========================
    # DATASET HISTORY
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS dataset_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        dataset_name TEXT,

        rows_count INTEGER,

        columns_count INTEGER,

        quality_score REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(project_id)
        REFERENCES projects(id)

    )

    """)

    # ==========================
    # SETTINGS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS settings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        theme TEXT DEFAULT 'Dark',

        language TEXT DEFAULT 'English',

        notifications INTEGER DEFAULT 1,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    # ==========================
    # NOTIFICATIONS
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS notifications(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        title TEXT,

        message TEXT,

        status TEXT DEFAULT 'Unread',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    conn.commit()

    conn.close()


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    create_database()

    print("Database Initialized Successfully")


# ==========================================
# ADD USER
# ==========================================

def add_user(full_name, email, mobile, password_hash):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO users(

        full_name,
        email,
        mobile,
        password_hash

    )

    VALUES(?,?,?,?)

    """, (

        full_name,
        email,
        mobile,
        password_hash

    ))

    conn.commit()

    conn.close()


# ==========================================
# GET USER
# ==========================================

def get_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE email=?

    """, (

        email,

    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================================
# CREATE PROJECT
# ==========================================

def create_project(user_id, project_name, description=""):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO projects(

        user_id,

        project_name,

        description

    )

    VALUES(?,?,?)

    """, (

        user_id,

        project_name,

        description

    ))

    conn.commit()

    conn.close()

# ==========================================
# GET PROJECT BY ID
# ==========================================

def get_project(project_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM projects
        WHERE id = ?
        """,
        (project_id,)
    )

    project = cursor.fetchone()

    conn.close()

    return project


# ==========================================
# DELETE PROJECT
# ==========================================

def delete_project(project_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM projects
        WHERE id = ?
        """,
        (project_id,)
    )

    conn.commit()

    conn.close()


# ==========================================
# SAVE ACTIVITY
# ==========================================

def save_activity(user_id, activity):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO activity_logs(

        user_id,

        activity

    )

    VALUES(?,?)

    """, (

        user_id,

        activity

    ))

    conn.commit()

    conn.close()

# ==========================================
# SAVE DATASET
# ==========================================

def save_dataset(
    project_id,
    file_name,
    file_path,
    file_type,
    file_size,
    total_rows,
    total_columns
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO uploaded_files(

        project_id,

        file_name,

        file_path,

        file_type,

        file_size,

        total_rows,

        total_columns

    )

    VALUES(?,?,?,?,?,?,?)

    """, (

        project_id,

        file_name,

        file_path,

        file_type,

        file_size,

        total_rows,

        total_columns

    ))

    conn.commit()

    conn.close()

# ==========================================
# SAVE LOGIN HISTORY
# ==========================================

def save_login(user_id, status="Success"):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO login_history(

        user_id,

        login_time,

        status

    )

    VALUES(

        ?,

        CURRENT_TIMESTAMP,

        ?

    )

    """, (

        user_id,

        status

    ))

    conn.commit()

    conn.close()


# ==========================================
# GET USER PROJECTS
# ==========================================

def get_user_projects(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM projects

    WHERE user_id=?

    ORDER BY id DESC

    """, (

        user_id,

    ))

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================
# GET RECENT ACTIVITIES
# ==========================================

def get_recent_activity(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM activity_logs

    WHERE user_id=?

    ORDER BY id DESC

    LIMIT 20

    """, (

        user_id,

    ))

    data = cursor.fetchall()

    conn.close()

    return data

if __name__ == "__main__":
    initialize_database()

# ==========================================
# GET PROJECT FILES
# ==========================================

def get_project_files(project_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM uploaded_files

    WHERE project_id = ?

    ORDER BY id DESC

    """, (project_id,))

    files = cursor.fetchall()

    conn.close()

    return files


def get_dataset_by_id(dataset_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM uploaded_files

    WHERE id = ?

    """,(dataset_id,))

    data = cursor.fetchone()

    conn.close()

    return data