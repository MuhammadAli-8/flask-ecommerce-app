from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FloatField, RadioField
from wtforms.validators import DataRequired, Length, Optional


class AddProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=240)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    price = FloatField("Price", validators=[DataRequired()])
    price_before = FloatField("Old Price", validators=[Optional()])
    stock = IntegerField("How much in stock?", validators=[DataRequired()])
    note = TextAreaField("note", validators=[Optional(), Length(max=2000)])
    category = SelectField("Category", validators=[DataRequired()], choices=[
        ('smartphone', 'Smartphone'),
        ('camera', 'Camera'),
        ('laptop', 'Laptop'),
        ('pc', 'PC'),
        ('accessory', 'Accessory'),
        ('headphone', 'Headphone'),
        ('watch', 'Watch'),
        ('other', 'Other')
    ])
    brand = SelectField("Brand", validators=[DataRequired()], choices=[
        ('samsung', 'Samsung'),
        ('apple', 'Apple'),
        ('xiaomi', 'Xiaomi'),
        ('oppo', 'Oppo'),
        ('sony', 'Sony'),
        ('anker', 'Anker'),
        ('other', 'Other')
    ])
    color = StringField("Color", validators=[Optional(), Length(max=50)])
    size = StringField("Size", validators=[Optional(), Length(max=50)])
    weight = FloatField("Weight", validators=[Optional()], default=0.1)
    camera = StringField("Camera", validators=[Optional(), Length(max=120)])
    screen = StringField("Screen", validators=[Optional(), Length(max=50)])
    ram = StringField("RAM", validators=[Optional(), Length(max=50)])
    cpu = StringField("CPU", validators=[Optional(), Length(max=120)])
    gpu = StringField("GPU", validators=[Optional(), Length(max=50)])
    os = StringField("OS", validators=[Optional(), Length(max=50)])
    storage = StringField("Storage", validators=[Optional(), Length(max=120)])
    battery = StringField("Battery", validators=[Optional(), Length(max=50)])
    pictures = MultipleFileField("Pictures", validators=[FileAllowed(['jpg', 'png']), FileRequired()])
    submit = SubmitField('Add Product')
    
    
class ReviewForm(FlaskForm):
    review = TextAreaField('Your Review', validators=[Optional()])
    rating = RadioField('Your Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=240)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    price = FloatField("Price", validators=[DataRequired()])
    price_before = FloatField("Old Price", validators=[Optional()])
    stock = IntegerField("How much in stock?", validators=[DataRequired()])
    note = TextAreaField("note", validators=[Optional(), Length(max=2000)])
    category = SelectField("Category", validators=[DataRequired()], choices=[
        ('smartphone', 'Smartphone'),
        ('camera', 'Camera'),
        ('laptop', 'Laptop'),
        ('pc', 'PC'),
        ('accessory', 'Accessory'),
        ('headphone', 'Headphone'),
        ('watch', 'Watch'),
        ('other', 'Other')
    ])
    brand = SelectField("Brand", validators=[DataRequired()], choices=[
        ('samsung', 'Samsung'),
        ('apple', 'Apple'),
        ('xiaomi', 'Xiaomi'),
        ('oppo', 'Oppo'),
        ('sony', 'Sony'),
        ('anker', 'Anker'),
        ('other', 'Other')
    ])
    color = StringField("Color", validators=[Optional(), Length(max=50)])
    size = StringField("Size", validators=[Optional(), Length(max=50)])
    weight = FloatField("Weight", validators=[Optional()], default=0.1)
    camera = StringField("Camera", validators=[Optional(), Length(max=120)])
    screen = StringField("Screen", validators=[Optional(), Length(max=50)])
    ram = StringField("RAM", validators=[Optional(), Length(max=50)])
    cpu = StringField("CPU", validators=[Optional(), Length(max=120)])
    gpu = StringField("GPU", validators=[Optional(), Length(max=50)])
    os = StringField("OS", validators=[Optional(), Length(max=50)])
    storage = StringField("Storage", validators=[Optional(), Length(max=120)])
    battery = StringField("Battery", validators=[Optional(), Length(max=50)])
    submit = SubmitField('Updadte Product')
