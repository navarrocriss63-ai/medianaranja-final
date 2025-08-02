
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'comercios.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    comercios = conn.execute('SELECT * FROM comercios').fetchall()
    conn.close()
    return render_template('index.html', comercios=comercios)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        imagen = request.form['imagen']
        rubro = request.form['rubro']
        conn.execute('INSERT INTO comercios (nombre, direccion, imagen, rubro) VALUES (?, ?, ?, ?)',
                     (nombre, direccion, imagen, rubro))
        conn.commit()
        return redirect('/admin')
    comercios = conn.execute('SELECT * FROM comercios').fetchall()
    conn.close()
    return render_template('admin.html', comercios=comercios)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM comercios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
