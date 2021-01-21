from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from forms import Tempform, LoginForm, FeedbackForm, RegistrationForm, SearchForm, ProductForm, PriceForm, ControlForm, ResetForm, TimeForm, UpdateForm, CartForm, DiscountForm, DetailsForm, PaymentForm, TimeForm1
from models import Temp, User, Product, Cart, Detail, Order, Feedback
import shelve
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import datetime, date, time, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'






@app.route("/")
@app.route("/home")
def home():
    db = shelve.open('storage.db', 'c')
    db["online"] = {}
    db["cart"] = {}
    db["error"] = {}
    #db["total"] = {}
    
    
    # db["Product"]={}
    # db["number"]=0
    # db["estore"]={}
    # db["Temp"]={}
    # db["Order"] = {}

    db.close()
    session['logged_in'] = False
    session['customer'] = False
    return render_template('index.html')

@app.route("/")
@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if session.get('customer'):
        form = FeedbackForm()
        if form.validate_on_submit():
            db = shelve.open('storage.db', 'c')
            dat = date.today()
            feed = {}
            try:
                feed = db["feedback"]
            except:
                print("error")
            fd = Feedback(form.name.data, form.number.data, form.rating.data, form.feedback.data, dat)
            feed[fd.get_fcount()] = fd
            db["feedback"] = feed
            print(db["feedback"])
            db.close()
            return redirect(url_for('e_store'))
        return render_template('feedback.html', form=form)

@app.route("/")
@app.route("/staff_feedback")
def staff_feedback():
    return render_template('staff_feedback.html')

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

        temp = Temp(form.nric.data, form.temperature.data, dat, current_time, form.symptoms.data, form.contact.data)
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
    db = shelve.open('storage.db', 'w')
    if db["error"] == "Integer only":
        flash("Integer only!", "danger")
        db["error"] = {}
    else:
        pass
    product_dict = {}
    product_dict = db['Product']
    print(db["Product"])
    product_list = []
    email = db["online"]
    for key in product_dict:
        entry = product_dict.get(key)
        product_list.append(entry)
    form = SearchForm()
    price_form = PriceForm()
    cart_form = CartForm()
    if cart_form.validate_on_submit():
        pass
    elif price_form.validate_on_submit():
        price_list = []
        for j in product_list:
            prices = j.get_price()
            if price_form.price.data >= prices:
                price_list.append(j)
        product_list = price_list
        return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form, cart_form=cart_form)
    elif form.validate_on_submit():
        search_list = []
        for i in product_list:
            item = i.get_title()
            if form.search.data.casefold() in item.casefold():
                search_list.append(i)
        product_list = search_list
        return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form, cart_form=cart_form)
    return render_template('customer_menu.html', product_list=product_list, form=form, price_form=price_form, cart_form=cart_form)


@app.route("/")
@app.route("/checkout1", methods=['GET', 'POST'])
def checkout1():
    if session.get('customer'):
        db = shelve.open('storage.db', 'c')
        order_dict = {}
        order_list = []
        order_dict = db["cart"]
        for key in order_dict:
                entry = order_dict.get(key)
                order_list.append(entry)
        
        form = DetailsForm()
        total = db["total"]
        total = float(total)
        if form.validate_on_submit():
            detail_dict = {}
            dat = date.today()
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            try:
                detail_dict = db['Detail']

            except:
                print("Error")
            
            detail = Detail(form.name.data, form.address.data, dat, current_time)
            detail_dict = detail
            db["Detail"] = detail_dict
            print(detail_dict)
            return redirect(url_for('checkout2'))

        return render_template('checkout_one.html', form=form, order_list=order_list, total=total)


@app.route("/")
@app.route("/checkout2", methods=['GET', 'POST'])
def checkout2():
    if session.get('customer'):
        form = PaymentForm()
        db = shelve.open('storage.db', 'c')
        cart = db["cart"]
        receipt_dict={}
        receipt_list = []
        receipt_dict = cart
        for key in receipt_dict:
            entry = receipt_dict.get(key)
            receipt_list.append(entry)
        total = db["total"]
        total = float(total)
        if form.validate_on_submit():
            
            email = db["online"]
            detail = db["Detail"]
            order_dict = {}
            user_dict = {}
            try:
                order_dict = db['Order']
                user_dict = db[email]
            except:
                print("Error")
            order = Order(detail.get_name(), detail.get_address(), detail.get_date(), detail.get_time(), form.name.data, form.card.data, form.date.data, form.code.data, cart, total, email)
            order_dict[order.get_order_id()] = order
            user_dict[order.get_order_id()] = order
            db['Order'] = order_dict
            db[email] = user_dict
            print(db[email])
            print(db['Order'])
            db.close()
            return redirect(url_for('checkout3'))

        return render_template('checkout_two.html', form=form, receipt_list=receipt_list, total=total)
    else:
        return redirect(url_for("e_store"))


@app.route("/")
@app.route("/checkout3", methods=['GET', 'POST'])
def checkout3():
    if session.get('customer'):
        db = shelve.open('storage.db', 'c')
        db["cart"] = {}
        db["total"] = {}
        return render_template('checkout_three.html')
    else:
        return redirect(url_for("e_store"))

@app.route("/")
@app.route("/estore_cart", methods=['GET', 'POST'])
def e_store_cart():
    if session.get('customer'):
        db = shelve.open('storage.db', 'c')
        cart = {}
        cart_list = []
        cart = db["cart"]
        for key in cart:
            entry = cart.get(key)
            cart_list.append(entry)
        total = 0
        for prod in cart_list:
            sub = prod.get_subtotal()
            total += float(sub)
        total_sub = "{:.2f}".format(total)
        total += 3
        total = "{:.2f}".format(total)
        form = DiscountForm()
        if form.validate_on_submit():
            print("hi")
            if form.code.data.upper() == "CODEHERO20":
                total_sub = "{:.2f}".format(float(total_sub) * 0.8)
                total = "{:.2f}".format(float(total_sub) + 3)
                db["total"] = total
                return render_template("customer_cart.html", cart_list=cart_list, total=total, total_sub=total_sub, form=form)
            else:
                flash("Discount Code not Applicable!", 'danger')
        db["total"] = total
        return render_template("customer_cart.html", cart_list=cart_list, total=total, total_sub=total_sub, form=form)
    else:
        return redirect(url_for("e_store"))


@app.route("/")
@app.route("/estore_order", methods=['GET', 'POST'])
def e_store_order():
    if session.get('customer'):
        db = shelve.open('storage.db', 'c')
        email = db['online']
        order_dict = {}
        order_list = []
        time_form = TimeForm1()
        search_form = SearchForm()
        time_list = []
        search_list = []
        try:
            order_dict = db[email]
        except:
            print("error")
        for key in order_dict:
            entry = order_dict.get(key)
            order_list.append(entry)
        if search_form.validate_on_submit():
            for s in order_list:
                search1 = s.get_order_id()
                if search_form.search.data in search1:
                    search_list.append(s)
            order_list = search_list
            return render_template("customer_orders.html", order_list=order_list, email=email, time_form=time_form, search_form=search_form)
        if time_form.validate_on_submit():
            for t in order_list:
                time_check = t.get_date1()
                if time_form.date.data == time_check:
                    time_list.append(t)
            order_list = time_list
            return render_template("customer_orders.html", order_list=order_list, email=email, time_form=time_form, search_form=search_form)
        return render_template("customer_orders.html", order_list=order_list, email=email, time_form=time_form, search_form=search_form)
        
    else:
        return redirect(url_for("e_store"))

@app.route('/delete_customer_order/<string:id>', methods=['POST'])
def remove_customer_order(id):
    if session.get('customer'):
        print('hi')
        db = shelve.open('storage.db', 'w')
        email = db["online"]
        order_dict = db[email]
        entry = order_dict.pop(id)
        db[email] = order_dict
        db.close()
        return redirect(url_for('e_store_order'))
    else:
        return redirect(url_for('e_store'))

@app.route("/add/<string:id>", methods=["GET", 'POST'])
def e_store_add(id):
    if session.get('customer'):
        
        db = shelve.open('storage.db', 'c')
        customer_dict = {}
        email = db["online"]
        try:
            customer_dict = db['cart']
        except:
            print("error") 
        
        product_dict = db["Product"]
        entry = product_dict.pop(id)
        quantity_data = request.form['quantity']
        try:
            quantity_data = int(quantity_data)
        except ValueError:
            db["error"] = "Integer only"
            return redirect(url_for("e_store"))  
        cart = Cart(entry, quantity_data)
        customer_dict[id] = cart
        db["cart"] = customer_dict
        db.close()
        print(customer_dict)
        return redirect(url_for("e_store"))

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
                    cus_email = i.get_email()
                    db["online"] = cus_email
                    print("exist")
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
    return render_template('admin_login.html', form=form)


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
@app.route("/admin_save", methods=['GET', 'POST'])
def save():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        save = {}
        try:
            save = db["save"]
        except:
            print('error')
        date = request.form['time']
        num = request.form['num']
        save[date] = num
        db["save"] = save
        print(db["save"])
        print('success')
        db.close()
        return redirect(url_for('staff_home'))
        



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
        search_form = SearchForm()
        reset_form = ResetForm()
        time_form = TimeForm()
        if time_form.search.data and time_form.validate():
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
            return render_template('temp-records.html', temp_list=temp_list, search_form=form, reset_form=reset_form, time_form=time_form)
        if search_form.submit.data and search_form.validate():
            db.close()
            search_list = []
            for j in temp_list:
                nric_check = j.get_ic_num()
                if search_form.search.data.casefold() in nric_check.casefold():
                    search_list.append(j)
            temp_list = search_list
            return render_template('temp-records.html', temp_list=temp_list, search_form=search_form, reset_form=reset_form, time_form=time_form)
        if reset_form.reset.data and reset_form.validate():
            db["Temp"] = {}
            temp_dict = db['Temp']
            temp_list = []
            return render_template('temp-records.html', temp_list=temp_list, search_form=search_form, reset_form=reset_form, time_form=time_form)

        return render_template('temp-records.html', temp_list=temp_list, search_form=search_form, reset_form=reset_form, time_form=time_form)
    else:
        return redirect(url_for('staff_login'))


@app.route("/")
@app.route("/delete_record", methods=['GET', 'POST'])
def delete():
    if session.get('logged_in'):
        if request.method == 'POST':
            print("hi")
            db = shelve.open('storage.db', 'c')
            temp_dict = db["Temp"]
            for getid in request.form.getlist('mycheckbox'):
                print(getid)
                entry = temp_dict.pop(int(getid))
                print(entry)
            db["Temp"] = temp_dict
            return redirect(url_for('staff_records'))




@app.route("/")
@app.route("/admin_graph", methods=['GET', 'POST'])
def staff_graph():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        save = {}
        try:
            save = db["save"]
        except:
            print('error')
        i = 1
        label = []
        val = []
        while i < 6:
            days = datetime.now() - timedelta(days=i)
            days = days.strftime("%Y-%m-%d")
            label.append(days)
            value = save.get(days)
            print(value)
            val.append(value)
            i+=1
        print(label)
        print(val)

        legend = "# of Customers"
        labels = label
        values = val
        backgroundColor = ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)"]
        borderColor = ["rgba(255,99,132,1)", "rgba(54, 162, 235, 1)"]
        return render_template('store-entry-graph.html', values=values, labels=labels, legend=legend, borderColor=borderColor, backgroundColor=backgroundColor)
    else:
        return redirect(url_for('staff_login'))

@app.route("/")
@app.route("/admin_shop_graph", methods=['GET', 'POST'])
def shop_graph():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        orders = {}
        orders_list = []
        label = []
        val = []
        try:
            orders = db["Order"]
        except:
            print("error")
        for key in orders:
            entry = orders.get(key)
            orders_list.append(entry)
        i = 0
        while i < 5:
            days = datetime.now() - timedelta(days=i)
            days = days.strftime("%Y-%m-%d")
            label.append(days)
            num = 0
            for count in orders_list:
                if str(count.get_date1()) == days:
                    num += 1
                    print(num)
            val.append(num)
            print(num)
            i+=1
        print(label)
        print(val)


            
        legend = "# of Orders"
        labels = label
        values = val
        backgroundColor = ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)"]
        borderColor = ["rgba(255,99,132,1)", "rgba(54, 162, 235, 1)"]
        return render_template('shop-graph.html', values=values, labels=labels, legend=legend, borderColor=borderColor, backgroundColor=backgroundColor)

@app.route("/")
@app.route("/admin_order", methods=['GET', 'POST'])
def shop_order():
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'c')
        order_dict = {}
        order_list = []
        time_form = TimeForm1()
        search_form = SearchForm()
        time_list = []
        search_list = []
        try:
            order_dict = db['Order']
        except:
            print("error")
        
        for key in order_dict:
            entry = order_dict.get(key)
            order_list.append(entry)
        if search_form.validate_on_submit():
            for s in order_list:
                search1 = s.get_order_id()
                if search_form.search.data in search1:
                    search_list.append(s)
            order_list = search_list
            return render_template("admin_orders.html", order_list=order_list, time_form=time_form, search_form=search_form)
        if time_form.validate_on_submit():
            for t in order_list:
                time_check = t.get_date1()
                if time_form.date.data == time_check:
                    time_list.append(t)
            order_list = time_list
            return render_template("admin_orders.html", order_list=order_list, time_form=time_form, search_form=search_form)
        return render_template("admin_orders.html", order_list=order_list, time_form=time_form, search_form=search_form)
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
        update_form = UpdateForm()
        if update_form.validate_on_submit():
            pass
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
            return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form, update_form=update_form)
        elif price_form.validate_on_submit():
            db.close()
            price_list = []
            for j in product_list:
                prices = j.get_price()
                if price_form.price.data >= prices:
                    price_list.append(j)
            product_list = price_list
            return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form,  update_form=update_form)

        return render_template('admin_menu.html', product_list=product_list, form=form, product_form=product_form, price_form=price_form,  update_form=update_form)
    else:
        return redirect(url_for('staff_login'))


@app.route('/delete_order/<string:id>', methods=['POST'])
def remove_order(id):
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'w')
        order_dict = db["Order"]
        entry = order_dict.pop(id)
        db["Order"] = order_dict
        db.close()
        return redirect(url_for('shop_order'))
    else:
        return redirect(url_for('staff_login'))

@app.route('/delete/<string:id>', methods=['POST'])
def remove(id):
    if session.get('logged_in'):
        
        db = shelve.open('storage.db', 'w')
        product_dict = db["Product"]
        

        entry = product_dict.pop(id)
        print(entry)
        db["Product"] = product_dict
        db.close()
        return redirect(url_for('staff_estore'))
    else:
        return redirect(url_for('staff_login'))

@app.route('/updateProduct/<string:id>/', methods=['POST'])
def update(id):
    if session.get('logged_in'):
        db = shelve.open('storage.db', 'w')
        product_dict = db["Product"]
        product = product_dict.get(id)
        product.set_title(request.form["title"])
        product.set_info(request.form["info"])
        product.set_price(request.form["price"])
        db["Product"] = product_dict
        db.close()
        return redirect(url_for('staff_estore'))
    else:
        return redirect(url_for('staff_login'))



if __name__ == '__main__':
    app.run(debug=True)