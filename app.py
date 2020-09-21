from itertools import groupby
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string'


@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT i.id, i.done, i.content, l.title \
                          FROM items i JOIN lists l \
                          ON i.list_id = l.id ORDER BY l.title;').fetchall()

    lists = {}

    for k, g in groupby(todos, key=lambda t: t['title']):
        lists[k] = list(g)

    conn.close()
    return render_template('index.html', lists=lists)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        content = request.form['content']
        list_title = request.form['list']
        new_list = request.form['new_list']

        # If a new list title is submitted, add it to the database
        if list_title == 'New List' and new_list:
            conn.execute('INSERT INTO lists (title) VALUES (?)',
                         (new_list,))
            conn.commit()
            # Update list_title to refer to the newly added list
            list_title = new_list

        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);',
                                 (list_title,)).fetchone()['id']
        conn.execute('INSERT INTO items (content, list_id) VALUES (?, ?)',
                     (content, list_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    lists = conn.execute('SELECT title FROM lists;').fetchall()

    conn.close()
    return render_template('create.html', lists=lists)

@app.route('/<int:id>/do/', methods=('POST',))
def do(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:id>/undo/', methods=('POST',))
def undo(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()

    todo = conn.execute('SELECT i.id, i.list_id, i.done, i.content, l.title \
                         FROM items i JOIN lists l \
                         ON i.list_id = l.id WHERE i.id = ?', (id,)).fetchone()

    lists = conn.execute('SELECT title FROM lists;').fetchall()

    if request.method == 'POST':
        content = request.form['content']
        list_title = request.form['list']

        if not content:
            flash('Content is required!')
            return redirect(url_for('edit', id=id))

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);',
                                 (list_title,)).fetchone()['id']

        conn.execute('UPDATE items SET content = ?, list_id = ?\
                      WHERE id = ?',
                     (content, list_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo, lists=lists)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
