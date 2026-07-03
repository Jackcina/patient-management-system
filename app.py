from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doj TEXT,
            patient_name TEXT,
            phone_no TEXT,
            dob TEXT,
            age INTEGER,
            sex TEXT,
            duration TEXT,
            disease TEXT,
            before_value TEXT,
            after_value TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()

create_database()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        doj = request.form["doj"]
        patient_name = request.form["patient_name"]
        phone_no = request.form["phone_no"]
        dob = request.form["dob"]
        age = request.form["age"]
        sex = request.form["sex"]
        duration = request.form["duration"]
        disease = request.form["disease"]
        before_value = request.form["before_value"]
        after_value = request.form["after_value"]
        notes = request.form["notes"]
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients
            (doj,patient_name,phone_no,dob, age, sex, duration, disease, before_value, after_value,notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doj,
            patient_name,
            phone_no,
            dob,
            age,
            sex,
            duration,
            disease,
            before_value,
            after_value,
            notes
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    search = request.args.get("search")

    if search:
      cursor.execute("""
        SELECT * FROM patients
        WHERE patient_name LIKE ?
        OR disease LIKE ?
    """, ('%' + search + '%', '%' + search + '%'))
    else:
       cursor.execute("SELECT * FROM patients")

    patients = cursor.fetchall()

    conn.close()

    return render_template("index.html", patients=patients)
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home")+ "#records")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    if request.method == "POST":
        doj = request.form["doj"]
        patient_name = request.form["patient_name"]
        phone_no = request.form["phone_no"]
        dob = request.form["dob"]
        age = request.form["age"]
        sex = request.form["sex"]
        duration = request.form["duration"]
        disease = request.form["disease"]
        before_value = request.form["before_value"]
        after_value = request.form["after_value"]
        notes = request.form["notes"]
        cursor.execute("""
            UPDATE patients
            SET doj=?, patient_name=?,phone_no=?, dob=?, age=?, sex=?, duration=?,
                disease=?, before_value=?, after_value=?, notes=?
            WHERE id=?
        """, (
            doj,
            patient_name,
            phone_no,
            dob,
            age,
            sex,
            duration,
            disease,
            before_value,
            after_value,
            notes,
            id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template("edit.html", patient=patient)
if __name__ == "__main__":
    app.run(debug=True)