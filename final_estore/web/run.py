from flask import Flask, render_template, url_for, flash, redirect, session
from forms import Tempform, LoginForm, RegistrationForm
from models import Temp, User
import shelve
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'







@app.route("/")
@app.route("/home")
def home():
    session['logged_in'] = False
    session['customer'] = False
    return render_template('temp-records.html')


@app.route("/")
@app.route("/temp_screen", methods=['GET', 'POST'])
def temp_screen():
    form = Tempform()
    if form.validate_on_submit():
        print("works")
        temp_dict = {}
        now = datetime.now()
        db = shelve.open('storage.db', 'c')
        dat = date.today()
        current_time = now.strftime("%H:%M:%S")
        try:
            temp_dict = db['Temp']
        except:
            print("Error")

        temp = Temp(form.nric.data, form.temperature.data, dat, current_time)
        temp_dict[temp.get_count_id()] = temp
        db['Temp'] = temp_dict
        db.close()
        if form.temperature.data > 37.5:
            return render_template('temp-error.html')
        return render_template('temp-success.html')
    return render_template('temp-screening.html', form=form)


@app.route("/")
@app.route("/live_counter")
def live_counter():
    return render_template('live-counter.html')

@app.route("/")
@app.route("/estore", methods=['GET', 'POST'])
def e_store():
    return render_template('customer_menu.html')


@app.route("/")
@app.route("/estore_register", methods=['GET', 'POST'])
def e_store_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("registering")
        users_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            users_dict = db['estore']
        except:
            print("error")   
        users_dict = db['estore']
        
        users_list = []
        for key in users_dict:
            entry = users_dict.get(key)
            users_list.append(entry)
        for i in users_list:
            user_mail = i.get_email()
            if user_mail == form.email.data:
                flash("An account have already been linked to this email!", 'danger')
                return redirect(url_for('e_store_register'))
            else:
                print("email available")
        users = User(form.email.data, form.password.data)
        users_dict[users.get_user_id()] = users
        db['estore'] = users_dict
        db.close()
        flash("Account registered!", 'success')
        print("registered")
        return redirect(url_for("e_store_login"))
    return render_template("signup.html", form=form)


@app.route("/")
@app.route("/estore_login", methods=['GET', 'POST'])
def e_store_login():
    form = LoginForm()
    if form.validate_on_submit():
        estore_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            estore_dict = db['estore']
        except:
            print("error")
        estore_dict = db['estore']
        db.close()
        estore_list = []
        for key in estore_dict:
            entry = estore_dict.get(key)
            estore_list.append(entry)
        for i in estore_list:
            user_mail = i.get_email()
            if user_mail == form.email.data:
                user_pass = i.get_password()
                if user_pass == form.password.data:
                    print("pass")
                    session["customer"] = True
                    return redirect(url_for('e_store'))
                else:
                    flash("Wrong Password!", 'danger')
                    return redirect(url_for('e_store_login'))
            
        flash("Email dont exist!", 'danger')
    return render_template('customer_login.html', form=form)

@app.route("/")
@app.route("/admin_login", methods=['GET', 'POST'])
def staff_login():
    admin_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
        admin_dict = db['Admin']
    except:
        print("error")
    admin_dict["test@gmail.com"] = "apscwinsac"
    db["Admin"] = admin_dict
    db.close()
    form = LoginForm()
    if form.validate_on_submit():
        print("validate")
        db = shelve.open('storage.db', 'r')
        if db["Admin"][form.email.data] == form.password.data:
            db.close()
            print("pass")
            session['logged_in'] = True
            return redirect(url_for('staff_home'))
        else:
            flash("Wrong email or Password!", 'danger')
    return render_template('login.html', form=form)


@app.route("/")
@app.route("/admin_home", methods=['GET', 'POST'])
def staff_home():
    if session.get('logged_in'):
        return render_template('staff-live-counter.html')
    else:
        return redirect(url_for('staff_login'))

@app.route("/")
@app.route("/admin_records", methods=['GET', 'POST'])
def staff_records():
    if session.get('logged_in'):
        temp_dict = {}
        db = shelve.open('storage.db', 'r')
        temp_dict = db['Temp']
        db.close()
        temp_list = []
        for key in temp_dict:
            entry = temp_dict.get(key)
            temp_list.append(entry)
        return render_template('temp-records.html', temp_list=temp_list)
    else:
        return redirect(url_for('staff_login'))


@app.route("/")
@app.route("/admin_graph", methods=['GET', 'POST'])
def staff_graph():
    if session.get('logged_in'):
        return render_template('store-entry-graph.html')
    else:
        return redirect(url_for('staff_login'))


if __name__ == '__main__':
    app.run(debug=True)