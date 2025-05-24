import matplotlib
matplotlib.use('Agg')
import io
import base64
import matplotlib.pyplot as plt
from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from app.models.user import User
from app.models.password import Password
from app.services.auth_service import authenticate_user, register_user
from app.services.password_service import generate_password, evaluate_entropy, detect_template_structure
from app.services.breach_checker import is_password_breached

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if register_user(email, password):
            flash('Регистрация успешна. Войдите в систему.')
            return redirect(url_for('login'))
        else:
            flash('Пользователь уже существует.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            session['user_id'] = user.id
            return redirect(url_for('vault'))
        else:
            flash('Неверный email или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/vault')
def vault():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    passwords = Password.query.filter_by(user_id=user_id).all()
    return render_template('vault.html', passwords=passwords)

@app.route('/generate_password')
def generate_password_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    password = generate_password()
    entropy = evaluate_entropy(password)
    breached = is_password_breached(password)
    template_like = detect_template_structure(password)
    return render_template('generated.html',
                           password=password,
                           entropy=entropy,
                           breached=breached,
                           template_like=template_like)

@app.route('/save_password', methods=['POST'])
def save_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    password = request.form['password']
    entropy = float(request.form['entropy'])
    user_id = session['user_id']
    new_password = Password(user_id=user_id, value=password, entropy=entropy)
    db.session.add(new_password)
    db.session.commit()
    flash('Пароль успешно сохранён.')
    return redirect(url_for('vault'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    passwords = Password.query.filter_by(user_id=user_id).all()
    entropies = [p.entropy for p in passwords]

    # График распределения энтропии
    fig, ax = plt.subplots()
    ax.hist(entropies, bins=10, color='skyblue', edgecolor='black')
    ax.set_title('Распределение энтропии паролей')
    ax.set_xlabel('Энтропия')
    ax.set_ylabel('Количество')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    # Дополнительная аналитика
    weak_count = sum(1 for p in passwords if detect_template_structure(p.value))
    breached_count = sum(1 for p in passwords if is_password_breached(p.value))

    return render_template(
        'dashboard.html',
        plot_url=plot_url,
        passwords=passwords,
        weak_count=weak_count,
        breached_count=breached_count
    )

