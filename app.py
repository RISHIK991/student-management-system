import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Absolute path for database (IMPORTANT for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            branch TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Initialize DB when app starts
init_db()


@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, branch) VALUES (?, ?)",
            (name, branch),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]

        conn.execute(
            "UPDATE students SET name=?, branch=? WHERE id=?",
            (name, branch, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,),
    ).fetchone()
    conn.close()

    return render_template("edit.html", student=student)


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
