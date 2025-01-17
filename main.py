from flask import Flask, redirect, request, jsonify, render_template, session, url_for
from database import attendance, create_connection, create_table, delete_subject, marks, register_students,  register_teachers, student_sigin, students_list, subject_list, teacher_sigin

app = Flask(__name__)

app.secret_key = 'SNN'

# home page
@app.route('/')
def index():
    return render_template('index.html')

#register page
@app.route('/register')
def register():
    return render_template('register.html')

# register students
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        batch = request.form['batch']
        phone = request.form['phone']
        password = request.form['password']
        
        if register_students(name, email, batch, phone, password):
            return render_template('index.html')
        
        else:
            print('error')
        
    return render_template('register_student.html')

# register teachers
@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if register_teachers(name, email, phone, password):
            return render_template('index.html')
        
        else:
            print('error')
        
    return render_template('register_teacher.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')        

@app.route('/signin_student', methods=['GET', 'POST'])
def signin_student():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if student_sigin(email, password):
            session['email'] = email 
            return redirect(url_for('student_dashboard'))

        else:
            return jsonify({"message": "Invalid email or password."}), 401
    return render_template('signin_student.html')

@app.route('/signin_teacher', methods=['GET', 'POST'])
def signin_teacher():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if teacher_sigin(email, password):
            session['email'] = email 
            return redirect(url_for('teacher_dashboard'))

        else:
            return jsonify({"message": "Invalid email or password."}), 401
    return render_template('signin_teacher.html')

# student dashboard
@app.route('/dashboard_student')
def student_dashboard():
    if 'email' in session:
        email = session['email']

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
        student = cursor.fetchone()

        if not student:
            return "Student not found", 404

        student_id = student[0]

        cursor.execute("""
            SELECT s.subject_name, m.marks, a.status
            FROM subjects s
            LEFT JOIN student_subjects ss ON s.id = ss.subject_id
            LEFT JOIN marks m ON ss.subject_id = m.subject_id AND m.student_id = ?
            LEFT JOIN attendance a ON ss.subject_id = a.subject_id AND a.student_id = ?
            WHERE ss.student_id = ?
        """, (student_id, student_id, student_id))

        results = cursor.fetchall()
        conn.close()

        return render_template('dashboard_student.html', results=results, student_id=student_id)
    else:
        return redirect(url_for('signin_student'))
    
# teachers dashboard
@app.route('/dashboard_teacher')
def teacher_dashboard():
    if 'email' in session:
        students = students_list()
        subjects = subject_list()
        return render_template('dashboard_teacher.html', email=session['email'], students= students, subjects = subjects)
    return redirect(url_for('signin_teacher'))

# TODO ee function database ilek aakanam flask render veenda
# students data teachers dashboard il kanikunu
# @app.route('/students')
# def students():
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, name FROM students")
#     student_list = cursor.fetchall()
#     conn.close()
    
#     return render_template('students.html', students=student_list)

@app.route('/add_subject', methods=['POST'])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subjects WHERE subject_name = ?", (subject_name,))
        existing_subject = cursor.fetchone()

        if existing_subject:
            return redirect(url_for('teacher_dashboard', message="Subject already exists."))

        cursor.execute("INSERT INTO subjects (subject_name) VALUES (?)", (subject_name,))
        subject_id = cursor.lastrowid 

        cursor.execute("SELECT id FROM students")
        students = cursor.fetchall()

        for student in students:
            cursor.execute("INSERT INTO student_subjects (student_id, subject_id) VALUES (?, ?)", (student[0], subject_id))

        conn.commit()
        conn.close()

        return redirect(url_for('teacher_dashboard'))




@app.route('/student/<int:student_id>', methods=['GET', 'POST'])
def student_actions(student_id):
    if request.method == 'POST':
        if 'add_marks' in request.form:
            subject_id = request.form['subject_id']
            marks_value = request.form['marks']
            # print(student_id, subject_id, marks_value)
            marks(student_id, subject_id, marks_value)
            
        elif 'add_attendance' in request.form:
            subject_id = request.form['subject_id']
            status = request.form['attendance']
           # print(student_id, subject_id, status)
            attendance(student_id, subject_id, status)

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.subject_name FROM subjects s
        JOIN student_subjects ss ON s.id = ss.subject_id
        WHERE ss.student_id = ?
    """, (student_id,))
    student_subjects = cursor.fetchall()
    conn.close()

    return render_template('student_actions.html', student_id=student_id, subjects=student_subjects)

@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
def del_subject(subject_id):
    if delete_subject(subject_id):
        return redirect(url_for('teacher_dashboard'))
    else:
        return redirect(url_for('teacher_dashboard', message='Error deleting subject.'))



if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

    app.run(debug=True)


    