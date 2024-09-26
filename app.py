from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'estoque.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        categoria = request.form['categoria']
        
        if not nome or not quantidade or not categoria:
            flash('Por favor, preencha todos os campos!')
            return redirect(url_for('add'))

        conn = get_db_connection()
        conn.execute('INSERT INTO produtos (nome, quantidade, categoria) VALUES (?, ?, ?)',
                     (nome, quantidade, categoria))
        conn.commit()
        conn.close()

        flash('Produto adicionado com sucesso!')
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        quantidade = request.form['quantidade']
        
        if not quantidade:
            flash('Quantidade não pode estar vazia!')
            return redirect(url_for('edit', id=id))

        conn.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (quantidade, id))
        conn.commit()
        conn.close()

        flash('Estoque atualizado com sucesso!')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_product.html', produto=produto)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Produto removido com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
