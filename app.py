from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Ruta absoluta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(BASE_DIR, "database", "practica.db")

def crear_base_datos():
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT,
            pasatiempos TEXT,
            me_gusta TEXT
        )
    """)
    conexion.commit()
    conexion.close()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/saludar", methods=["POST"])
def f_saludar():
    nombre = request.form["nombre"]
    fecha_nacimiento = request.form.get("fecha_nacimiento", "")
    pasatiempos = request.form.getlist("pasatiempos")
    me_gusta = request.form["me_gusta"]
    
    pasatiempos_texto = ", ".join(pasatiempos)
    
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, fecha_nacimiento, pasatiempos, me_gusta)
        VALUES (?, ?, ?, ?)
    """, (nombre, fecha_nacimiento, pasatiempos_texto, me_gusta))
    conexion.commit()
    conexion.close()
    
    return render_template(
        "saludar.html",
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        pasatiempos=pasatiempos,
        me_gusta=me_gusta
    )

@app.route("/alumnos")
def listar_alumnos():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alumnos ORDER BY id")
    alumnos = cursor.fetchall()
    conexion.close()
    
    return render_template(
        "listar_alumnos.html",
        alumnos=alumnos
    )

crear_base_datos()

if __name__ == "__main__":
    app.run(debug=True)
