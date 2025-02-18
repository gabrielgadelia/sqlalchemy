from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from forms import LoginForm, RegistrationForm, UserUpdateForm

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy import Integer, String, SmallInteger, BigInteger

app = Flask(__name__)


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base, session_options={'autocommit': True})

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str]
    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]


# with app.app_context():
#     print('Creating Database And Tables')
#     db.create_all()
#     print('Created Database and tablesss')


def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value


def create_conn():
    conn = sqlite3.connect('mziuri.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_cursor(conn):
    return conn.cursor()


def close_conn(conn):
    return conn.close()


app.jinja_env.filters['middle'] = middle


@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'nugzari', 'svianadze'
    num = 25
    d = {'name': 'nugzari', 'age': 20}
    return render_template('home.html', first_name=first_name,
                           last_name=last_name, num=num, d=d)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('forma validuria')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            age = form.age.data
            address = form.address.data

            # conn = create_conn()
            # cursor = create_cursor(conn)
            # cursor.execute("""
            # select * from users where email = ?
            # """, (email,))
            # user_exists = cursor.fetchone()
            # close_conn(conn)
            user_exists = User.query.filter_by(first_name=first_name).all()
            if user_exists is not None:
                # flash('User With This Email Already Exists!')
                form.first_name.errors = ['User With This First Name Already Exists!']
                return render_template('register.html', form=form)

            # conn = create_conn()
            # cursor = create_cursor(conn)
            # cursor.execute("""
            # insert into users (first_name, last_name, email, age, birth_date, password) values
            # (?, ?, ?, ?, ?, ?)
            # """, (first_name, last_name, email, age, birthday, password))
            # conn.commit()
            # close_conn(conn)
            user = User(first_name=first_name, last_name=last_name,
                        age=age, address=address)
            db.session.add(user)
            # db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

app.secret_key = 'ijbiazbadub84v8rbsibiewfvidvsa'


@app.route('/users')
def users():
    form = UserUpdateForm()
    # conn = create_conn()
    # cursor = create_cursor(conn)
    # cursor.execute("select * from users")
    # users = cursor.fetchall()
    # close_conn(conn)
    users_data = User.query.all()
    return render_template('users.html', users=users_data, form=form)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    # form = UserUpdateForm()
    # conn = create_conn()
    # cursor = create_cursor(conn)
    # first_name = form.first_name.data
    # last_name = form.last_name.data
    # age = form.age.data
    # user = cursor.execute("""
    # select * from users where id = ?
    # """, (user_id, ))
    # if not user.fetchone():
    #     flash('User With This Id Does Not Exist!')
    #     return redirect(url_for('users'))
    # cursor.execute("""
    # update users set first_name = ?, last_name = ?, age = ? where id = ?
    # """, (first_name, last_name, age, user_id))
    # flash("User Updated Successfully!!!!")
    # conn.commit()
    # close_conn(conn)
    return redirect(url_for('users'))


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = create_conn()
    cursor = create_cursor(conn)
    user = cursor.execute("""
        select * from users where id = ?
        """, (user_id,))
    if not user.fetchone():
        flash('User With This Id Does Not Exist!')
        return redirect(url_for('users'))
    cursor.execute("""
    delete from users where id = ?
    """, (user_id,))
    flash("User Successfully Deleted!!!!!")
    conn.commit()
    close_conn(conn)
    return redirect(url_for('users'))
if __name__ == '__main__':
    app.run(debug=True, port=5100)
