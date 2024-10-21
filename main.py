from flask import Flask, request, jsonify, render_template
from database import create_connection, create_table, register_students,  register_teachers

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        batch = request.form['batch']
        phone = request.form['phone']
        password = request.form['password']
        
        if register_students(name, email, batch, phone, password):
            return jsonify({"message": "Student registered successfully."}), 200
        
        else:
            print('error')
        
    return render_template('register_student.html')

@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if register_teachers(name, email, phone, password):
            return jsonify({"message": "Teacher registered successfully."}), 200
        
        else:
            print('error')
        
    return render_template('register_teacher.html')

        
if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

    app.run(debug=True)


    