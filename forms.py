from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from models import User, Category

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Masuk')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Nama Lengkap', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Konfirmasi Password', validators=[
        DataRequired(), EqualTo('password', message='Password harus sama')])
    role = SelectField('Role', choices=[('penjual', 'Penjual'), ('pembeli', 'Pembeli')], validators=[DataRequired()])
    phone = StringField('Nomor Telepon')
    address = TextAreaField('Alamat')
    submit = SubmitField('Daftar')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah digunakan. Pilih username lain.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah terdaftar. Gunakan email lain.')

class ProductForm(FlaskForm):
    title = StringField('Judul Produk', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Deskripsi', validators=[DataRequired(), Length(min=10)])
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    condition = SelectField('Kondisi', choices=[
        ('New', 'Baru'),
        ('Like New', 'Seperti Baru'),
        ('Good', 'Baik'),
        ('Fair', 'Cukup'),
        ('Poor', 'Buruk')
    ], validators=[DataRequired()])
    
    # Point calculation factors
    utility_score = IntegerField('Nilai Kegunaan (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    scarcity_score = IntegerField('Nilai Kelangkaan (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    durability_score = IntegerField('Nilai Daya Tahan (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    portability_score = IntegerField('Nilai Portabilitas (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    seasonal_score = IntegerField('Nilai Musiman (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    
    images = FileField('Gambar Produk (Maksimal 5)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Hanya file gambar yang diperbolehkan!')
    ])
    
    submit = SubmitField('Simpan Produk')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

class ChatMessageForm(FlaskForm):
    message = TextAreaField('Pesan', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Kirim')

class OfferForm(FlaskForm):
    product_ids = HiddenField('Product IDs')
    message = TextAreaField('Pesan Penawaran', validators=[Length(max=500)])
    submit = SubmitField('Kirim Penawaran')

class TrackingForm(FlaskForm):
    tracking_number = StringField('Nomor Resi', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Update Resi')
