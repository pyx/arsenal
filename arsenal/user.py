"""arsenal.user - user blueprint"""

from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    render_template,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from .forms import (
    ChangeEmailForm,
    ChangeNameForm,
    ChangePasswordForm,
    LoginForm,
)
from .models import User, db


login_manager = LoginManager()
login_manager.login_view = 'user.login'


user = Blueprint(
    'user', __name__, template_folder='templates', static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_app(app):
    login_manager.init_app(app)


def check_password(user, password):
    return user and user.is_active and user.check_password(password)


def is_unique(field, data):
    user = User.query.filter(
        db.and_(field.like(data), db.not_(User.id == current_user.id))).first()
    return not user


@user.route('/')
@login_required
def dashboard():
    return render_template('user/dashboard.html')


@user.route('/change/email/', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if is_unique(User.email, form.email.data):
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash('Email changed, sign in with this one next time')
            return redirect(request.args.get('next') or url_for('.dashboard'))
        flash('This email is already taken')
    return render_template('user/change_email.html', form=form)


@user.route('/change/name/', methods=['GET', 'POST'])
@login_required
def change_name():
    form = ChangeNameForm()
    if form.validate_on_submit():
        if is_unique(User.name, form.name.data):
            current_user.name = form.name.data
            db.session.add(current_user)
            db.session.commit()
            flash('User name changed')
            return redirect(request.args.get('next') or url_for('.dashboard'))
        flash('This user name is already taken')
    return render_template('user/change_name.html', form=form)


@user.route('/change/password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.password = form.newpass.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password changed')
            return redirect(request.args.get('next') or url_for('.dashboard'))
        flash('Incorrect password')
    return render_template('user/change_password.html', form=form)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if check_password(user, form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully.')
            return redirect(request.args.get('next') or url_for('.dashboard'))
        flash('Invalid email or password')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('.login'))


@user.route('/<int:id>/')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('user/profile.html', user=user)
