from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import os

app = Flask(__name__)
PATH = "fabrica.db"

def get_db():
    conn = sqlite3.connect(PATH)
    conn.row_factory = sqlite3.Row
    return conn

def start_db():
    # Remove o arquivo do banco se existir para recriar
    if os.path.exists(PATH):
        os.remove(PATH)
    
    db = get_db()
    # Cria a tabela diretamente no código
    db.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            curso TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()
    print("Banco de dados inicializado com sucesso!")

@app.route("/")
def index():
    db = get_db()
    alunos = db.execute("SELECT * FROM alunos").fetchall()
    db.close()
    return render_template("index.html", alunos=alunos)

@app.route("/cadastro", methods=["GET", "POST"])  
def cadastro(): 
    if request.method == "POST":  
        nome = request.form["nome"]  
        idade = request.form["idade"]  
        curso = request.form["curso"] 
        
        db = get_db()
        db.execute("INSERT INTO alunos (nome, idade, curso) VALUES (?,?,?)", (nome, idade, curso)) 
        db.commit()
        db.close()
        
        return redirect(url_for("index"))
    return render_template("cadastro.html")

if __name__ == "__main__":
    start_db()
    app.run(debug=True)
