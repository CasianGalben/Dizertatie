from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from .models import db, Carte, User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/cartiAfisare', methods=['GET'])
def get_carti():
    carti = Carte.query.all()
    return jsonify([{'titlu': carte.titlu, 'autor': carte.autor, 'an': carte.an} for carte in carti])

@main.route('/carti')
def show_carti():
    carti = Carte.query.all()
    return render_template('carti.html', carti=carti)

@main.route('/login')
def login():
    # Asigură-te că formularul din login.html trimite datele aici
    return render_template('login.html')

@main.route('/proceseaza_login', methods=['POST'])
def proceseaza_login():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Ai fost conectat cu succes!', 'success')
        return redirect(url_for('main.profile'))  # Redirecționează la profil după autentificare
    else:
        flash('Utilizator inexistent.', 'danger')
        return redirect(url_for('main.login'))

@main.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)  # Asigură-te că acest template afișează datele utilizatorului

@main.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    if request.method == 'POST':
        if user is None:
            user = User()  # Creează un nou utilizator dacă nu este niciunul în sesiune
            db.session.add(user)
        
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.faculty = request.form['faculty']
        user.year = request.form.get('year', type=int)
        user.gender = request.form['gender']

        file = request.files['profile_picture']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('path_to_your_upload_folder', filename)
            file.save(filepath)
            user.profile_picture = filepath

        db.session.commit()
        flash('Profilul a fost actualizat cu succes.', 'success')

    return render_template('profile_update.html', user=user if user else {})
@main.route('/BunVenit')
def bun_venit():
    if 'user_id' in session:
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.login'))
