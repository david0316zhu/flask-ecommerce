from flask import Flask, render_template, url_for, flash, redirect, session
from forms import Tempform, LoginForm, RegistrationForm, SearchForm, ProductForm, PriceForm, ControlForm, ResetForm, TimeForm, UpdateForm
from models import Temp, User, Product
import shelve
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import datetime, date, time

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'






@app.route("/")
@app.route("/home")
def home():
    db = shelve.open('storage.db', 'c')
    db["customer"] = {}
    db.close()
    session['logged_in'] = False
    session['customer'] = False
    return render_template('index.html')


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
        current_time = now.strftime("%H:%M")
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
    db = shelve.open('storage.db', 'r')
    if db["number"] > 999:
        db["number"] = 0
        hundred = "0"
        ten = "0"
        one = "0"
        return render_template('live-counter.html', hundred=hundred, ten=ten, one=one)
    elif db["number"] > 9 and db["number"] < 100:
        hundred = "0"
        num = str(db["number"])
        ten = num[0]
        one = num[1]
        return render_template('staff-live-counter.html', hundred=hundred, ten=ten, one=one)
    elif db["number"] > 99 and db["number"] < 1000:
        num = str(db["number"])
        hundred = num[0]
        ten = num[1]
        one = num[2]
        return render_template('live-counter.html', hundred=hundred, ten=ten, one=one)
    else: 
        hundred = "0"
        ten = "0"
        one = str(db["number"])
        return render_template('live-counter.html', hundred=hundred, ten=ten, one=one)
    

@app.route("/")
@app.route("/estore", methods=['GET', 'POST'])
def e_store():
    db = shelve.open('storage.db', 'r')
    product_dict = {}
    product_dict = db['Product']
    print(db["Product"])
    product_list = []
    for key in product_dict:
        entry = product_dict.get(key)
        product_list.append(entry)
    form = SearchForm()
    price_form = PriceForm()
    if price_form.validate_on_submit():
        price_list = []
        for j in product_list:
            prices = j.get_price()
            if price_form.price.data >= prices:
                price_list.append(j)
        product_list = price_list
        return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form)
    if form.validate_on_submit():
        search_list = []
        for i in product_list:
            item = i.get_title()
            if form.search.data.casefold() in item.casefold():
                search_list.append(i)
        product_list = search_list
        return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form)
    return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form)


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
        db = shelve.open('storage.db', 'w')
        try:
            estore_dict = db['estore']
        except:
            print("error")
        estore_dict = db['estore']
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
                    db["customer"] = i
                    return redirect(url_for('e_store'))
                else:
                    flash("Wrong Password!", 'danger')
                    return redirect(url_for('e_store_login'))
            
        flash("Email dont exist!", 'danger')
    return render_template('customer_login.html', form=form)


@app.route("/")
@app.route("/estore_cart", methods=['GET', 'POST'])
def e_store_cart():
    if session.get('customer'):
        db = shelve.open('storage.db', 'r')
        customer = db["customer"]
        db.close()
        print(customer.get_email())
        return render_template("customer_cart.html")
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
        if form.email.data == "test@gmail.com":
            if db["Admin"][form.email.data] == form.password.data:
                db.close()
                print("pass")
                session['logged_in'] = True
                return redirect(url_for('staff_home'))
            else:
                flash("Wrong email or Password!", 'danger')
        else:
            flash("Wrong email or Password!", 'danger')
    return render_template('login.html', form=form)


@app.route("/")
@app.route("/admin_home", methods=['GET', 'POST'])
def staff_home():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        if db["number"] > 999:
            db["number"] = 0
            hundred = "0"
            ten = "0"
            one = "0"
            
        elif db["number"] > 9 and db["number"] < 100:
            hundred = "0"
            num = str(db["number"])
            ten = num[0]
            one = num[1]
            
        elif db["number"] > 99 and db["number"] < 1000:
            num = str(db["number"])
            hundred = num[0]
            ten = num[1]
            one = num[2]
            
        else: 
            hundred = "0"
            ten = "0"
            one = str(db["number"])
            
        
        
        control_form = ControlForm()
        
        if control_form.validate_on_submit():
            if control_form.add.data:
                db["number "] = 0
                db["number"] +=1
                if db["number"] > 999:
                    db["number"] = 0
                    hundred = "0"
                    ten = "0"
                    one = "0"
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                elif db["number"] > 9 and db["number"] < 100:
                    hundred = "0"
                    num = str(db["number"])
                    ten = num[0]
                    one = num[1]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                elif db["number"] > 99 and db["number"] < 1000:
                    num = str(db["number"])
                    hundred = num[0]
                    ten = num[1]
                    one = num[2]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                else: 
                    hundred = "0"
                    ten = "0"
                    one = str(db["number"])
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
            
            if control_form.remove.data:
                db["number"] -= 1
                if db["number"] < 0:
                    db["number"] = 999
                    num = str(db["number"])
                    hundred = num[0]
                    ten = num[1]
                    one = num[2]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                elif db["number"] < 10:
                    num = str(db["number"])
                    hundred = "0"
                    ten = "0"
                    one = num[0]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                
                elif db["number"] < 100:
                    num = str(db["number"])
                    hundred = "0"
                    ten = num[0]
                    one = num[1]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
                elif db["number"] > 100 and db["number"] < 1000:
                    num = str(db["number"])
                    hundred = num[0]
                    ten = num[1]
                    one = num[2]
                    return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)

        return render_template('staff-live-counter.html', control_form=control_form, hundred=hundred, ten=ten, one=one)
    else:
        return redirect(url_for('staff_login'))

@app.route("/")
@app.route("/admin_records", methods=['GET', 'POST'])
def staff_records():
    if session.get('logged_in'):
        temp_dict = {}
        db = shelve.open('storage.db', 'w')
        temp_dict = db['Temp']
        temp_list = []
        
        for key in temp_dict:
            entry = temp_dict.get(key)
            temp_list.append(entry)
        form = SearchForm()
        reset_form = ResetForm()
        time_form = TimeForm()
        if time_form.validate_on_submit():
            db.close()
            time_list = []
            for t in temp_list:
                time_check = t.get_date()
                if time_form.date.data == time_check:
                    time1 = datetime.strftime(time_form.time1.data, '%H:%M')
                    time2 = datetime.strftime(time_form.time2.data, '%H:%M')
                    time3  = t.get_time()
                    
                    if time3 >= time1 and time3 <= time2:
                        time_list.append(t)
            temp_list = time_list
            return render_template('temp-records.html', temp_list=temp_list, form=form, reset_form=reset_form, time_form=time_form)
        if form.validate_on_submit():
            db.close()
            search_list = []
            for j in temp_list:
                nric_check = j.get_ic_num()
                if form.search.data.casefold() in nric_check.casefold():
                    search_list.append(j)
            temp_list = search_list
            return render_template('temp-records.html', temp_list=temp_list, form=form, reset_form=reset_form, time_form=time_form)
        if reset_form.validate_on_submit():
            db["Temp"] = {}
            temp_dict = db['Temp']
            temp_list = []
            return render_template('temp-records.html', temp_list=temp_list, form=form, reset_form=reset_form, time_form=time_form)
        return render_template('temp-records.html', temp_list=temp_list, form=form, reset_form=reset_form, time_form=time_form)
    else:
        return redirect(url_for('staff_login'))


@app.route("/")
@app.route("/admin_graph", methods=['GET', 'POST'])
def staff_graph():
    if session.get('logged_in'):
        return render_template('store-entry-graph.html')
    else:
        return redirect(url_for('staff_login'))

@app.route("/")
@app.route("/admin_shop_graph", methods=['GET', 'POST'])
def shop_graph():
    if session.get('logged_in'):
        return render_template('shop-graph.html')
    else:
        return redirect(url_for('staff_login'))


@app.route("/")
@app.route("/admin_estore", methods=['GET', 'POST'])
def staff_estore():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        product_dict = {}
        try:
            product_dict = db['Product']
        except:
            print("error")
        print(db['Product'])
        product_list = []
        for key in product_dict:
            entry = product_dict.get(key)
            product_list.append(entry)
        product_form = ProductForm()
        form = SearchForm()
        product_form = ProductForm()
        price_form = PriceForm()
        if product_form.validate_on_submit():
            new_product_dict = db["Product"]
            new_product = Product(product_form.title.data, product_form.info.data, product_form.price.data)
            new_product_dict[new_product.get_product_id()] = new_product
            db['Product'] = new_product_dict
            db.close()
            return redirect(url_for('staff_estore'))
        elif form.validate_on_submit():
            db.close()
            search_list = []
            for i in product_list:
                item = i.get_title()
                if form.search.data.casefold() in item.casefold():
                    search_list.append(i)
            product_list = search_list
            return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form)
        elif price_form.validate_on_submit():
            db.close()
            price_list = []
            for j in product_list:
                prices = j.get_price()
                if price_form.price.data >= prices:
                    price_list.append(j)
            product_list = price_list
            return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form)

        return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form)
    else:
        return redirect(url_for('staff_login'))

@app.route('/delete/<string:id>', methods=['POST'])
def remove(id):
    if session.get('logged_in'):
        
        db = shelve.open('storage.db', 'w')
        product_dict = db["Product"]
        

        entry = product_dict.pop(id)
        db["Product"] = product_dict
        db.close()
        
        db.close()
        return redirect(url_for('staff_estore'))
    else:
        return redirect(url_for('staff_login'))

@app.route('/updateProduct/<string:id>/', methods=['GET', 'POST'])
def update_product(id):
    if session.get('logged_in'):
        update_form = UpdateForm()
        if update_form.validate_on_submit():
            db = shelve.open('storage.db', 'w')
            product_dict = db["Product"]
            product = product_dict.get(id)
            product.set_title(update_form.title.data)
            product.set_info(update_form.info.data)
            product.set_price(update_form.price.data)
            db["Product"] = product_dict
            db.close()
            return redirect(url_for('staff_estore'))
        else:
            db = shelve.open('storage.db', 'w')
            product_dict = db["Product"]
            product = product_dict.get(id)
            update_form.title.data = product.get_title()
            update_form.info.data = product.get_info()
            update_form.price.data = product.get_price()

        return render_template('update_product.html', update_form=update_form)
    else:
        return redirect(url_for('staff_login'))


if __name__ == '__main__':
    app.run(debug=True)