from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'abcdefgh'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Image Are Allowed'),
            FileRequired('File Field Should Not Be Empty')
        ]
    )
    submit = SubmitField('Submit')


@app.route('/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    file_url = None
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    return render_template("index.html", form=form, file_url=file_url)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/registrasi')
def registrasi():
    return render_template("registrasi.html")


if __name__ == "__main__":
    app.run(debug=True)
