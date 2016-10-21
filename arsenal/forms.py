"""arsenal.forms - forms for arsenal"""

from flask_wtf import Form
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, Length, DataRequired


class EmailForm(Form):
    email = EmailField(
        'Email', validators=[DataRequired(), Email(), Length(max=120)])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])


class ChangeEmailForm(EmailForm):
    submit = SubmitField('Change')


class ChangeNameForm(Form):
    name = StringField(
        'New Name', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Change')


class ChangePasswordForm(PasswordForm):
    newpass = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('newpass')])
    submit = SubmitField('Change')


class LoginForm(EmailForm, PasswordForm):
    """User login form"""
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewPostForm(Form):
    content = TextAreaField('New Message', validators=[DataRequired()])
    submit = SubmitField('Post')


class UpdatePostForm(Form):
    content = TextAreaField('Edit Message', validators=[DataRequired()])
    submit = SubmitField('Update')


class NewTopicForm(Form):
    title = StringField(
        'New Topic', validators=[DataRequired(), Length(max=120)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
