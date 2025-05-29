from flask import Blueprint, render_template, request, redirect, session
from db import get_connection
from blockchain import Blockchain
import hashlib

vote_bp = Blueprint('vote_bp', __name__)
chain = Blockchain()

@vote_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = username
            if user['has_voted']:
                return "You have already voted!"
            return redirect('/vote')
        return "Invalid credentials"
    return render_template('login.html')

@vote_bp.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        vote_value = request.form['candidate']
        voter_hash = hashlib.sha256(str(session['user_id']).encode()).hexdigest()
        chain.create_block(voter_hash, vote_value)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET has_voted=1 WHERE id=%s", (session['user_id'],))
        conn.commit()

        return redirect('/confirmation')
    
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()
    return render_template('vote.html', candidates=candidates)

@vote_bp.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')
