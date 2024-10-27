import sqlite3
import bcrypt

# ivde database create cheytu
def create_connection():
    try:
        conn = sqlite3.connect('database.db3')
        return conn
    except sqlite3.Error as e:
        print(f"{e}")
    return conn

# ee function database il table create cheytu
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS students (
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       email TEXT UNIQUE,
                       batch TEXT,
                       phone TEXT,
                       passwrd TEXT
                       )
                       ''')
        
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS teachers (
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       email TEXT UNIQUE,
                       phone TEXT,
                       passwrd TEXT
                       )
                       ''')
        
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS subjects (
                       id INTEGER PRIMARY KEY,
                       subject_name TEXT UNIQUE
                       )
                       ''')

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS student_subjects (
                       student_id INTEGER,
                       subject_id INTEGER,
                       FOREIGN KEY(student_id) REFERENCES students(id),
                       FOREIGN KEY(subject_id) REFERENCES subjects(id),
                       PRIMARY KEY (student_id, subject_id)
                       )
                       ''')
        
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS marks (
                        id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        subject_id INTEGER,
                        marks INTEGER,
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(subject_id) REFERENCES subjects(id)
                        )
                       ''')
                    

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        subject_id INTEGER,
                        status TEXT,
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(subject_id) REFERENCES subjects(id)
                       )
                       ''')

        conn.commit()

    except sqlite3.Error as e:
        print(f"{e}")


# * students data database ilek write cheytu
def register_students(name, email, batch, phone, passwrd):
    conn = create_connection()
    cursor = conn.cursor()

    passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO students (name, email, batch, phone, passwrd) 
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, batch, phone, passwrd))

        conn.commit()

        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# * teachers data database ilek write cheytu
def register_teachers(name, email, phone, passwrd):
    conn = create_connection()
    cursor = conn.cursor()

    passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO teachers (name, email, phone, passwrd) 
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, passwrd))

        conn.commit()

        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# adding subjects
def subjects(student_id, subject_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO subjects (student_id, subject_name) 
            VALUES (?, ?)
        """, (student_id, subject_name))

        conn.commit()
        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# adding marks
def marks(student_id, subject_id, marks):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO marks (student_id, subject_id, marks) 
            VALUES (?, ?, ?)
        """, (student_id, subject_id, marks))

        conn.commit()
        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# add attendance
def attendance(student_id, subject_id, status):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO attendance (student_id, subject_id, status) 
            VALUES (?, ?, ?, ?)
        """, (student_id, subject_id, status))

        conn.commit()
        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# * signin student
def student_sigin(email, passwrd):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT passwrd FROM students WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            passwrd_hash = user[0]
            if bcrypt.checkpw(passwrd.encode('utf-8'), passwrd_hash):
                print("Sign-in successful.")
                return True
            else:
                print("Invalid email or password.")
                return False
        else:
            print("Invalid email or password.")
            return False
            
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

# * signin teacher
def teacher_sigin(email, passwrd):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT passwrd FROM teachers WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            passwrd_hash = user[0]
            if bcrypt.checkpw(passwrd.encode('utf-8'), passwrd_hash):
                print("Sign-in successful.")
                return True
            else:
                print("Invalid email or password.")
                return False
        else:
            print("Invalid email or password.")
            return False
            
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

def students_list():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    conn.close()
    return students
