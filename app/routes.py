from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
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
    # Presupun că ai un template 'login.html' pentru această rută
    return render_template('login.html')

@main.route('/proceseaza_login', methods=['POST'])
def proceseaza_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Ai fost conectat cu succes!', 'success')
        return redirect(url_for('main.profile'))
    else:
        flash('Nume de utilizator sau parolă incorectă.', 'danger')
        return redirect(url_for('main.login'))

@main.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Trebuie să te conectezi pentru a accesa această pagină.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash('Eroare la încărcarea profilului.', 'error')
        return redirect(url_for('main.login'))

    return render_template('profile.html', user=user)

@main.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.faculty = request.form['faculty']
    user.year = request.form.get('year', type=int)
    user.gender = request.form['gender']

    file = request.files['profile_picture']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('path_to_your_upload_folder', filename)  # Ajustează calea folderului
        file.save(filepath)
        user.profile_picture = filepath

    db.session.commit()
    flash('Profilul a fost actualizat cu succes.', 'success')
    return redirect(url_for('main.profile'))

@main.route('/BunVenit')
def bun_venit():
    if 'user_id' in session:
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.login'))


