from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from .models import db, Carte, User, Comentariu
from sqlalchemy.orm import joinedload

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
    return render_template('login.html')

@main.route('/proceseaza_login', methods=['POST'])
def proceseaza_login():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Ai fost conectat cu succes!', 'success')
        return redirect(url_for('main.profile'))
    else:
        flash('Utilizator inexistent.', 'danger')
        return redirect(url_for('main.login'))

@main.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@main.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
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

    return render_template('profile_update.html', user=user)

@main.route('/BunVenit')
def bun_venit():
    if 'user_id' in session:
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.login'))

@main.route('/search')
def search():
    query = request.args.get('query', '')
    search_pattern = f"%{query}%"
    matching_books = Carte.query.options(joinedload(Carte.comentarii)).filter(
        db.or_(
            Carte.titlu.like(search_pattern),
            Carte.autor.like(search_pattern),
            db.cast(Carte.an, db.String).like(search_pattern) 
        )
    ).all()
    return render_template('search_results.html', books=matching_books, query=query)

@main.route('/carte/<int:id_carte>', methods=['GET', 'POST'])
def detalii_carte(id_carte):
    carte = Carte.query.get_or_404(id_carte)
    comentarii = Comentariu.query.filter_by(id_carte=id_carte).all()
    if request.method == 'POST':
        action = request.form.get('action', 'Adauga')  

        if action == 'Adauga':
            continut_comentariu = request.form['continut']
            comentariu_nou = Comentariu(
                continut=continut_comentariu,
                id_carte=id_carte,
                id_utilizator=None  
            )
            db.session.add(comentariu_nou)
            db.session.commit()
        elif action.startswith('Sterge:'):
            comentariu_id = int(action.split(':')[1])  
            comentariu = Comentariu.query.get_or_404(comentariu_id)
            db.session.delete(comentariu)
            db.session.commit()

        return redirect(url_for('main.detalii_carte', id_carte=id_carte))
    
    return render_template('detalii_carte.html', carte=carte, comentarii=comentarii)


