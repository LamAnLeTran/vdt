from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=1,max=50)])
    username = StringField('User Name', [validators.length(min=4,max=25)])
    email = StringField('Email', [validators.length(min=6,max=50)])
    password = PasswordField('Password', [validators.data_required(), validators.equal_to('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm Password')