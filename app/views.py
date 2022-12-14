from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db
from .forms import UserForm, EmployeeForm
from .models import User, Employee


def index():
    employees = Employee.query.all()
    return render_template('index.html', empoyees=employees)


@login_required
def employee_create():
    form = EmployeeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Сотрудник успешно сохранен!', 'success')
            return redirect(url_for('index'))
    return render_template('employee_create.html', form=form)


def employee_detail(employee_id):
    employee = Employee.query.get(employee_id)

    return render_template('employee_detail.html', employee=employee)


@login_required
def employee_update(employee_id):
    employee = Employee.query.get(employee_id)
    form = EmployeeForm(request.form, obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Данные о сотруднике успешно изменены!', 'success')
            return redirect(url_for('index'))
    return render_template('employee_update.html', form=form)


@login_required
def employee_delete(employee_id):
    employee = Employee.query.get(employee_id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Сотрудник успешно удален!', 'success')
        return redirect(url_for('index'))
    return render_template('employee_delete.html', employee=employee)


def register_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {user.username} успешно зарегистрирован!', 'success')
            return redirect(url_for('auth_base'))
    return render_template('register.html', form=form)


def login_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # user = User()
            # form.populate_obj(user)
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Успешно авторизован!', 'primary')
                return redirect(url_for('auth_base'))
            else:
                flash('Неправильно введенные логин или пароль', 'danger')
    return render_template('login.html', form=form)


def logout_view():
    logout_user()
    return redirect(url_for('auth_base'))
