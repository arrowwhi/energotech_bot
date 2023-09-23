import sqlite3

conn = sqlite3.connect('base.db')
cur = conn.cursor()


def create_table_clients():
    cur.execute( '''create table clients (
    id integer primary key autoincrement,
    tg_id int,
    status text default 'OFF'
);
    ''')
    conn.commit()


def add_client(tg_id):
    cur.execute('''insert into clients (tg_id)
    values (?);''', tg_id)
    conn.commit()


def change_dialog_type(tg_id, turn_on=False):
    t = "ON" if turn_on else 'OFF'
    cur.execute('''update clients
    set status=?
    where tg_id=?;''', (t, tg_id))
    conn.commit()


def select_dialog_type(tg_id):
    cur.execute('''
    select status from clients
    where tg_id = ?;''', tg_id)
    return cur.fetchone()


