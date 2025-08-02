from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('comercios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comercios")
    comercios = cursor.fetchall()
    conn.close()
    return render_template('index.html', comercios=comercios)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        imagen = request.form['imagen']
        rubro = request.form['rubro']
        conn = sqlite3.connect('comercios.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comercios (nombre, direccion, imagen, rubro) VALUES (?, ?, ?, ?)",
                       (nombre, direccion, imagen, rubro))
        conn.commit()
        conn.close()
        return redirect('/admin')
    conn = sqlite3.connect('comercios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comercios")
    comercios = cursor.fetchall()
    conn.close()
    return render_template('admin.html', comercios=comercios)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('comercios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comercios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)