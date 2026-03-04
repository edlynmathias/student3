from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentname TEXT NOT NULL,
            sapid TEXT NOT NULL,
            gender TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    selected_student = None

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Add student
    if request.method == "POST" and "add_student" in request.form:
        studentname = request.form["studentname"]
        sapid = request.form["sapid"]
        gender = request.form["gender"]
        marks = request.form["marks"]

        cursor.execute("""
            INSERT INTO students (studentname, sapid, gender, marks)
            VALUES (?, ?, ?, ?)
        """, (studentname, sapid, gender, marks))
        conn.commit()

    # Fetch all students
    cursor.execute("SELECT id, studentname FROM students")
    students = cursor.fetchall()

    # If dropdown selected
    student_id = request.args.get("student_id")
    if student_id:
        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        selected_student = cursor.fetchone()

    conn.close()

    return render_template("index.html",
                           students=students,
                           selected_student=selected_student)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)