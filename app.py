from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("students.db")

@app.route("/")
def index():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    con.close()
    return render_template("index.html", students=data)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO students VALUES(NULL,?,?)",(name,branch))
        con.commit()
        con.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    con = get_db()
    cur = con.cursor()
    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]
        cur.execute("UPDATE students SET name=?, branch=? WHERE id=?",(name,branch,id))
        con.commit()
        return redirect("/")
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    con.close()
    return render_template("edit.html", student=student)

@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run()

