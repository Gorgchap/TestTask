from TestTask import app, db
from TestTask.models import User, Category, Commodity, BoughtCommodity
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import update
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST' and request.form.get('category'):
        sel = int(request.form.get('category'))
        comties = Commodity.query.filter(Commodity.category_id == sel, Commodity.rest > 0).all() if sel else Commodity.query.filter(Commodity.rest > 0).all()
        return render_template('index.html', boughtcomties=BoughtCommodity.query.filter_by(user_id=current_user.id).all(), comties=comties, catries=Category.query.all(), sel=sel)
    elif request.method == 'POST' and request.form.get('commodity'):
        sele, error = int(request.form.get('commodity')), None
        comty = Commodity.query.filter_by(id=sele).first()
        try:
            if int(request.form.get('count')) < 1:
                error = "Your value is not positive number"
            elif int(request.form.get('count')) > comty.rest:
                error = "Not enough number of things"
            elif int(request.form.get('count')) * comty.price > current_user.balance:
                error = "Not enough money"
            else:
                db.session.add(BoughtCommodity(buyer=current_user, comty=comty, count=int(request.form.get('count'))))
                Commodity.query.filter_by(id=sele).update({'rest': comty.rest - int(request.form.get('count'))})
                User.query.filter_by(id=current_user.id).update({'balance': current_user.balance - int(request.form.get('count')) * comty.price})
                db.session.commit()
        except ValueError:
            error = "Your value is not number"
        finally:
            return render_template('index.html', boughtcomties=BoughtCommodity.query.filter_by(user_id=current_user.id).all(), comties=Commodity.query.filter(Commodity.rest > 0).all(), catries=Category.query.all(), sele=sele, error=error)
    return render_template('index.html', boughtcomties=BoughtCommodity.query.filter_by(user_id=current_user.id).all(), comties=Commodity.query.filter(Commodity.rest > 0).all(), catries=Category.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None:
            return render_template('login.html', first='Invalid email')
        if not user.check_password(request.form['pass']):
            return render_template('login.html', second='Invalid password')
        login_user(user, remember=request.form.get("remember-me", False))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        first, second, before = None, None, False
        if User.query.filter_by(email=request.form['email']).first():
            first, before = 'Use another email', True
        if request.form['pass'] != request.form['pass2']:
            second, before = 'Password is not confirmed', True
        if before:
            return render_template('register.html', first=first, second=second)
        user = User(email=request.form['email'])
        user.set_password(request.form['pass'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')
