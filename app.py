from flask import Flask, redirect, render_template, request, url_for, abort, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
ENV = "dev"
if ENV == "dev":
    debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Alibaba2022@localhost/vcard'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jxouilcborkuey:327d3b88b76f7446d389669c2088c0bb898628d81f8680452b0010099db98070@ec2-54-83-21-198.compute-1.amazonaws.com:5432/d7phf22ceeljh0"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class userPage(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    company = db.Column(db.String(100))


class Image(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    mime = db.Column(db.String, nullable=False)
    uname = db.Column(db.String, nullable=False)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        role = request.form.get("role")
        company = request.form.get("company")
        email = request.form.get("email")
        phone = request.form.get("mobile")
        address = request.form.get("address")
        file = request.files['file']
        newUser = userPage(fname=(fname.lower()), lname=(lname.lower()), role=role, company=company,
                           email=email, phone=phone, address=address)
        db.session.add(newUser)
        db.session.commit()
        img = Image(
            name=secure_filename(file.filename),
            mime=file.mimetype,
            data=file.read(),
            uname=fname.lower()
        )
        db.session.add(img)
        db.session.commit()
        return redirect(f"/{fname}")

    return render_template("index.html")


@app.route("/<user>", methods=["POST", "GET"])
def page(user):

    userInfo = userPage.query.filter_by(fname=user.lower()).first()
    print(userInfo)
    fname = userInfo.fname
    lname = userInfo.lname
    role = userInfo.role
    email = userInfo.email
    phone = userInfo.phone
    address = userInfo.address
    userImg = Image.query.filter_by(uname=user.lower()).first()

    if lname == None:
        lname = ""
    else:
        lname = lname

    na = fname.capitalize() + " " + lname.capitalize()
    shlink = request.host_url+fname
    return render_template("user.html", shlink=shlink, na=na, phone=phone, mail=email, role=role, address=address, imga=userImg)


@app.route('/download/<int:image_id>')
def download(image_id):
    img = Image.query.get_or_404(image_id)
    return send_file(
        BytesIO(img.data),
        mimetype=img.mime,
        attachment_filename=img.name
    )


if __name__ == "__main__":
    app.run()
