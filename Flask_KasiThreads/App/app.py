from email.mime.image import MIMEImage
import random
import re
import smtplib
import ssl

from flask import Flask, flash, redirect, render_template, request, session, url_for
from models import kasithreads_db
import bcrypt
import os

from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

email_sender = 'happyseoketsa@gmail.com'
email_password = 'sstu ypai kfrz cgio'

# initial value for verifications
customer_verification_code = None 

app = Flask(__name__)
db = kasithreads_db(app)
#Folder to upload all the photos
app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.secret_key = 'jhgf7938r97b4-2w2883e2132./,,;d,fdeg'


#Main Website
@app.route('/website_home')
@app.route('/')
def website_home():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM brandlogo")
    brands = cursor.fetchall()
    cursor.execute("SELECT * FROM products ORDER BY id LIMIT 10")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM homephotos ORDER BY id DESC Limit 1")
    cheap = cursor.fetchone()
    cursor.close()
    return render_template('website/home.html', brands =brands, products =products, cheap=cheap)

@app.route('/newestbrands')
def newestbrands():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_type = 'brandowner' ORDER BY id DESC")
    brandowners = cursor.fetchall()

    # List to hold brand owners and their products
    brandnames = []

    for brandowner in brandowners:
        # Fetch brand name for each brand owner
        cursor.execute("SELECT brandname FROM users WHERE id = %s", (brandowner[0],))
        brandname_result = cursor.fetchone()
        if brandname_result:
            brandname = brandname_result[0]
            # Append the brand owner and their products to the list
            cursor.execute("SELECT * FROM products WHERE brand = %s", (brandname,))
            products = cursor.fetchall()
            for product in products:
                brandnames.append({
                    'brandname': brandname,
                    'product_id': product[0],
                    'product_name': product[1],
                    'product_description': product[2],
                    'product_filename': product[3],
                    'product_price': product[4],
                    'product_sizes': product[5],
            })


    return render_template('website/newestbrand.html', brandnames=brandnames)

@app.route('/brandproducts/<int:brand_id>')
def brandproducts(brand_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (brand_id,))

    products = cursor.fetchone()

    products = products[1]
    cursor.execute("SELECT * FROM products WHERE brand = %s", (products,))
    products = products = cursor.fetchall()
    cursor.close()
    if products:
        return render_template('website/brandproducts.html', products = products)
    else: 
        return redirect(url_for('website_home'))


#Sort By
@app.route('/shop', methods=['GET'])
def shop():
    sort_by = request.args.get('sort_by', 'name')  # Default sort by name
    
    cursor = db.connection.cursor()

    if sort_by == 'price_asc':
        query = "SELECT * FROM products ORDER BY price ASC"
    elif sort_by == 'price_desc':
        query = "SELECT * FROM products ORDER BY price DESC"
    elif sort_by == 'name_desc':
        query = "SELECT * FROM products ORDER BY name DESC"
    elif sort_by == 'name_asc':
        query = "SELECT * FROM products ORDER BY name ASC"
    else:
        query = "SELECT * FROM products ORDER BY name"

    cursor.execute(query)
    products = cursor.fetchall()

    db.connection.commit()
    cursor.close()

    return render_template('website/shop.html', products=products)

# Product Details
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    cursor = db.connection.cursor()

    # Fetch the product details
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    review_details = []

    if product:
        # Fetch reviews for the given product_id
        cursor.execute("SELECT * FROM reviews WHERE product_id = %s ORDER BY created_at ASC", (product_id,))
        reviews = cursor.fetchall()

        for review in reviews:
            # Fetch customer details for each review
            cursor.execute("SELECT * FROM customers WHERE id = %s", (review[3],))  # Assuming the customer_id is at index 3 in the reviews table
            customer = cursor.fetchone()
            review_details.append({
                'review': review,
                'customer': customer
            })

        sizes = product[5].split(',') if product[5] else []

        cursor.close()

        return render_template('website/product.html', product=product, sizes=sizes, review_details=review_details)
    else:
        cursor.close()
        return "Product not found"


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.connection.cursor()

        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        customer = cursor.fetchone()

        if customer is not None and customer[3]==email and bcrypt.checkpw(password.encode('utf-8'), customer[5].encode('utf-8')):
            session['customer_id'] = customer[0]
            session['customer_name'] = customer[1]
            session['customer_lastname'] = customer[2]
            return  redirect(url_for('website_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('account'))
    elif 'customer_name' in session:
        return redirect(url_for('useraccount'))
    else:
        return render_template('website/login.html')


# customer account page provided they are logged in 
@app.route('/useraccount')
def useraccount():
    name = session.get('customer_name')
    lastname = session.get('customer_lastname')
    return render_template('website/useraccount.html', name =name , lastname=lastname)

#customer lockout
@app.route('/website_logout')
def website_logout():
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    session.pop('customer_lastname', None)
    flash('Loggedout', 'danger')
    return redirect(url_for('account'))

# Take logged in customer reviews
@app.route('/reviews/<int:product_id>', methods=['POST', 'GET'])
def reviews(product_id):
    
    if 'customer_name' in session:
        customer_name = session['customer_name']
        review = request.form['review']
        cursor = db.connection.cursor()

        cursor.execute("Select * from customers where first_name = %s", (customer_name,))
        user = cursor.fetchone()
        cursor.execute("INSERT INTO reviews (description, product_id, customer_id) VALUES (%s, %s, %s)", (review, product_id, user[0]))
        db.connection.commit()
        cursor.close()

        return redirect(url_for('product_detail', product_id=product_id))
    else:
        return "Unauthorized", 401

    

@app.route('/register')
def register():
    return render_template('website/register.html')



@app.route('/website_register', methods =['POST', 'GET'])
def website_register():
    if request.method == 'POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        password = request.form['password']
        password2 = request.form['password2']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if password != password2:
            flash('Passwords Entered do not match', 'danger')
            return redirect('register')
        else:
            special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'
            if not re.search(special_char_pattern, password):
                flash('Make sure your password contains special characters', 'danger')
                return redirect('register')
            elif len(password) < 8:
                flash('Password too short, make sure is 8 characters long.', 'danger')
                return redirect('register')
            elif not phonenumber.isdigit():
                flash('Make sure phone number contains digits only', 'danger')
                return redirect('register')
            else:
                global customer_verification_code
                customer_verification_code = random.randint(10001, 99999)

                email_receiver = email
                subject = "Account Verification, from KasiThreads"
                body = f"""
<html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Jaini+Purva&family=Poetsen+One&display=swap" rel="stylesheet">
    </head>
    <body>
        <br><br>
        <div>Hi {firstname} {lastname}
            <br><br>
            USE THIS CODE TO VERIFY YOUR KASITHREADS ACCOUNT: <b style=" font-weight:800; font-size:20px">{customer_verification_code}</b>
            <br><br>
            Yours Sincerely,
            <br>
            KasiThreads Team.
        </div>

        <h1 style ="font-weight: 800; font-family: "Jaini Purva", system-ui; font-size: 35px; margin-left: 5%; margin-top: 15px;width: auto; ">KasiThreads</h1>
        <h2>Where Local Shines</h2>
    </body>
</html>


 """

                em = EmailMessage()
                em['From'] = email_sender
                em['To']= email_receiver
                em['subject']= subject
                em.set_content(MIMEText(body, 'html'))

                context = ssl.create_default_context()

                #Check if email exist in database
                cursor = db.connection.cursor()
                cursor.execute("SELECT * FROM customers WHERE email = %s", (email_receiver,))
                account = cursor.fetchone()

                if account:
                    flash('User email exist, login or press forgot password.','danger')
                    return redirect('account')
                else:
                    cursor.execute("INSERT INTO customers (first_name, last_name, email, phone_number, password_hash) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, email_receiver, phonenumber, hashed_password))
                    db.connection.commit()
                    cursor.close()

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                        flash('Email was sent to your email address with verification code.', 'success')
                        return redirect(url_for('verification'))
    return render_template('website/register.html')

#Customer Account verification
@app.route('/verification',methods =['POST', 'GET'])
def verification():
    global customer_verificantion_code
    if request.method == 'POST':
        verification = request.form['verify']
        if str(customer_verification_code) == str(verification):
            flash("Account created, you can now login", 'success')
            return redirect(url_for('account'))
        else: 
            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM customers ORDER BY id DESC LIMIT 1")
            db.connection.commit()
            cursor.close()
            flash('Verification code does not match the one send on email.','danger')
            return redirect(url_for('register'))
        
    return render_template('website/verification.html')

#Customer forgot Password
@app.route('/forgot_password', methods= ['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cursor = db.connection.cursor()
        cursor.execute("select * from customers where email = %s", (email,))
        account = cursor.fetchone()

        if account:
            global customer_verification_code
            customer_verification_code = random.randint(10001, 99999)

            email_receiver = email
            subject = "Verification Code, from KasiThreads"
            body = f"""
<html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Jaini+Purva&family=Poetsen+One&display=swap" rel="stylesheet">
    </head>
    <body>
        <br><br>
        <div>Hi {account[1]} {account[2]},
            <br><br>
            USE THIS CODE TO CHANGE YOUR KASITHREADS ACCOUNT PASSWORD: <b style=" font-weight:800; font-size:20px">{customer_verification_code}</b>
            <br><br>
            Ignore if you did not request an account password change.
            <br><br>
            Yours Sincerely,
            <br>
            KasiThreads Team.
        </div>

        <h1 style ="font-weight: 800; font-family: "Jaini Purva", system-ui; font-size: 35px; margin-left: 5%; margin-top: 15px;width: auto; ">KasiThreads</h1>
        <h2>Where Local Shines</h2>
    </body>
</html>
"""

            em = EmailMessage()
            em['From'] = email_sender
            em['To']= email_receiver
            em['subject']= subject
            em.set_content(MIMEText(body, 'html'))

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                session['forgotpassword_id']= account[0]
                return redirect(url_for('forgot_password_verification'))
        else:
            flash("Account does not exist", 'danger')
            return redirect(url_for('account'))


    return render_template('website/forgot_password.html')

# verification when a user request to change password(forgot password)
@app.route('/forgot_password_verification', methods= ['POST', 'GET'])
def forgot_password_verification():
    if request.method == 'POST':
        
        verification_code = customer_verification_code
        input_code = request.form['verify']

        if str(verification_code) == str(input_code):
            return redirect(url_for('change_password', id = id))
        else:
            flash('Incorrect verification code')
            return redirect(url_for('account'))
    
    return render_template('website/forgot_password_verification.html')

# Customer New Password
@app.route('/change_password', methods = ['POST','GET'])
def change_password():
    if request.method == 'POST':
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 == password2 :
            hashed_password =bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(hashed_password)
            
            if 'forgotpassword_id' in session:
                cursor = db.connection.cursor()
                cursor.execute('UPDATE customers SET password_hash = %s where id = %s', (hashed_password, session.get('forgotpassword_id')))
                db.connection.commit()
                session.pop('forgotpassword_id', None)
                flash('password changed successfully', 'success')
                return redirect(url_for('account'))
            else:
                return redirect(url_for('account'))
        else:
            flash('Passwords entered do not match', 'danger')
            return redirect(url_for('change_password'))
    return render_template('website/change_password.html')


@app.route('/about')
def about():
    return render_template('website/about.html')


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        session['cart_details'] = []
        data = request.get_json()
        cart_products = data.get('cart', [])

        cursor = db.connection.cursor()

        for cart_product in cart_products:
            cursor.execute('SELECT * FROM products WHERE id = %s', (cart_product['productId'],))
            product = cursor.fetchone()
            if product:
                final_product = {
                    'id': product[0],
                    'brand': product[7],
                    'name': product[1],
                    'size': cart_product['size'],
                    'quantity': cart_product['quantity'],
                    'price': product[4] * cart_product['quantity'],
                    'filename': product[3]
                }
                session['cart_details'].append(final_product)

        cursor.close()
        return redirect(url_for('cart'))

    cart_products = session.get('cart_details', [])
    total = sum(cart_product['price'] for cart_product in cart_products)
    
    return render_template('website/cart.html', cart_products=cart_products, total=total)

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        if 'cart_details' in session:
            product_ids = [item['id'] for item in session['cart_details']]
            quantities = [item['quantity'] for item in session['cart_details']]
            sizes = [item['size'] for item in session['cart_details']]

            session['product_ids'] = product_ids
            session['quantities'] = quantities
            session['sizes'] = sizes
            return redirect(url_for('orderdetails'))
    return render_template('website/cart.html')  

@app.route('/orderdetails', methods=['POST', 'GET'])
def orderdetails():
    if request.method == 'POST':
        if 'product_ids' in session:
            name = request.form.get('name')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            cellnumber = request.form.get('cellnumber')
            paxi_type = request.form.get('options')
            paxi_add = request.form.get('paxiaddress')
            order = []

            cursor = db.connection.cursor()
            for i in range(len(session['product_ids'])):
                cursor.execute(
                    "INSERT INTO orders (size, quantity, customer_email, paxi_add, name, lastname, paxi_type, product_id, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (session['sizes'][i], session['quantities'][i], email, paxi_add, name, lastname, paxi_type, session['product_ids'][i], cellnumber)
                )
                cursor.execute("select * from products where id = %s",(session['product_ids'][i],) )
                product =cursor.fetchone()
                order.append(product)
            db.connection.commit()


            email_receiver = email
            subject = "KasiThreads, Order Confirmation"
            body = f"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Jaini+Purva&family=Poetsen+One&display=swap" rel="stylesheet">
</head>
<body>
    <br><br>
    <div>Hi {name} {lastname},<br><br>
    Thank you, your Kasithreads order is being processed you will recieve communication from each brand when your products are delivered at PEP PAXI.
        <br><br>
     <h5 style="font-size:25px; background-color:gray">Ordered products</h5>
"""
            em = EmailMessage()
# Adding order details dynamically
            for i, product in enumerate(order):
                image_path = f'static/uploads/{product[3]}'  # Replace with your image path
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        img_data = img_file.read()
                        img_name = os.path.basename(image_path)
                        img_type = img_name.split('.')[-1]  # Extract image type dynamically
                        cid = f'image{i + 1}'
                        em.add_attachment(img_data, maintype='image', subtype=img_type, cid=cid)
                        body += f"""
                        <div style="display:flex; flex-direction:column ; border-bottom: 2px solid gray; gap:5%">
                            <img src="cid:{cid}" alt="{product[3]}" style="width:30%;height:3%;">
                            <div style="margin-left:10%">
                                <h3>{product[7]}</h3>
                                <h4 style="position:relative; bottom:40px">{product[1]}</h4>
                                <h4 style="position:relative; bottom:40px">Quantity: {session['quantities'][i]}</h4>  
                                <h4 style="position:relative; bottom:40px">Size: {session['sizes'][i]}<h4> 
                                <h3 style="position:relative; bottom:40px">R{product[4]} each</h3>       
                            </div>
                        </div>
                        <br>
"""

            body += """
                <br><br>

            <br>
                KasiThreads Team.
                </div>

                <h1 style="font-weight: 800; font-family: 'Jaini Purva', system-ui; font-size: 35px;margin-top: 15px;width: auto;">KasiThreads</h1>
                <h2>Where Local Shines</h2>
</body>
</html>
"""

            
            em['From'] = email_sender
            em['To'] = email_receiver    
            em['Subject'] = subject
            html_body = MIMEText(body, 'html')
            em.attach(html_body)


            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.send_message(em)
            
           

            # Clear the session data after processing the order
            session.pop('product_ids', None)
            session.pop('quantities', None)
            session.pop('sizes', None)


            return 'Order added'
    return render_template('website/checkout.html')

@app.route('/policies')
def policies():
    return render_template('website/policies.html')


#Dashboard
@app.route('/Dashboard_login', methods=['GET', 'POST'])
def Dashboard_login():
    if request.method == 'POST':
        brandname = request.form['brandname']
        password = request.form['password']

        cursor = db.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE brandname = %s", (brandname,))
        user = cursor.fetchone()

        if user is not None and user[1]==brandname and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_type'] = user[4]
            session['user_id'] = user[0]
            session['brandname'] = user[1]
            flash('Access Granted.', 'success')
            return  redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('Dashboard_login'))
    
    return render_template('dashboard/login.html')
#Logout
@app.route('/logout')
def logout():
    session.pop('user_type', None)
    session.pop('user_id', None)
    session.pop('brandname', None)
    return redirect(url_for('Dashboard_login'))

@app.route('/home')
def home():
    if 'brandname' in session:
        user = session.get('brandname')
        user_type = session.get('user_type')
        cursor = db.connection.cursor()
        user_id = session.get('user_id')
        cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
        brandlogo = cursor.fetchone()
        return render_template('dashboard/home.html', user =user, user_type = user_type, brandlogo=brandlogo)
    else:
        flash('Access denied. You must be logged in to access this page.')


@app.route('/home_photos')
def home_photos():
    if session.get('user_type') == 'admin':
        user_id = session.get('user_id')
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
        brandlogo = cursor.fetchone()
        flash("Access Granted, Note uploading new Pictures will change home pictures of the main website.", 'success')
        return render_template("dashboard/home_photos.html", brandlogo=brandlogo)
    else:
        flash("Access denied. You must be an admin to access this page.", 'danger')
        return redirect(url_for('home'))
    
@app.route('/uploadHome_photos', methods=['POST', 'GET'])
def uploadHome_photos():
    if session.get('user_type') == 'admin':
        if request.method == 'POST':
            homeLeft = request.files['homeLeft']
            homeRight_Top = request.files['homeRight_Top']
            homeRight_bottom = request.files['homeRight_Bottom']

            if homeLeft.filename != '' and homeRight_Top !='' and homeRight_bottom!='' :
                cursor = db.connection.cursor()
                file_homeLeft = homeLeft.filename
                file_homeRight_top = homeRight_Top.filename
                file_homeRight_bottom = homeRight_bottom.filename

                homeRight_Top.save(os.path.join(app.config['UPLOAD_FOLDER'],file_homeRight_top))
                homeRight_bottom.save(os.path.join(app.config['UPLOAD_FOLDER'],file_homeRight_bottom))
                homeLeft.save(os.path.join(app.config['UPLOAD_FOLDER'],file_homeLeft))

                cursor.execute("INSERT INTO homephotos (leftphoto, righttop, rightbottom) VALUES (%s, %s, %s)", (file_homeLeft, file_homeRight_top, file_homeRight_bottom))
               
                db.connection.commit()
                cursor.close()
                
                flash('Photo added','success')
                return redirect(url_for('home_photos'))
            else:
                flash('failed to upload photos', 'danger')
                return redirect(url_for('home_photos'))
    


@app.route('/brands')
def brands():
    if session.get('user_type') == 'admin':
        user = session.get('brandname')
        user_id = session.get('user_id')
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
        brandlogo = cursor.fetchone()
        flash('Access Granted. You can add new brand that meet Kasithreads criteria.', 'success')
        return render_template('dashboard/brands.html', user=user, brandlogo=brandlogo)
    
    else:
        flash('Access denied. You must be an kasithreads admin to access this page.', 'danger')
        return redirect(url_for('home'))

#Adding users into the dashboard
@app.route('/register_user', methods=['POST','GET'])
def register_user():
    if session.get('user_type') == 'admin':
        if request.method == 'POST':
            logo = request.files['logo']
            brandname = request.form['brandname']
            email = request.form['email']
            password = request.form['password']
            user_type = request.form['user_type']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            if logo.filename != '':
                cursor = db.connection.cursor()
                filename = logo.filename
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                cursor.execute("INSERT INTO users (brandname, email, password, user_type) VALUES (%s, %s, %s, %s)", (brandname, email, hashed_password, user_type))
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO brandlogo (logopath, brand_id) VALUES (%s,%s)", (filename,user_id))
                db.connection.commit()
                cursor.close()


                email_receiver = email
                subject = "KasiThreads Dashboard Logins"
                body = f"""
<html>
    <body>
        <br><br>
        <div>Dear {brandname},
            <br><br>
            Congradulations, your brand met KasiThreads criteria, and it is now one of the featured brands on our website.
            <br><br>
            Below are your login details to our dashboard, the link to the dashboard can be found on our website home page, at the footer(scroll down to the bottom, on your left click where written "Dashboard")
            <br><br>
            <h1> Username: {brandname}</h1>
            <h1> Password: {password}</h1>
            <h2> You are adviced to change your password after logging in</h2><br><br>
            Yours Sincerely,
            <br>
            KasiThreads Team.
        </div>

        <h1 style ="font-weight: 800; font-family: "Jaini Purva", system-ui; font-size: 35px; margin-left: 5%; margin-top: 15px;width: auto; ">KasiThreads</h1>
        <h2>Where Local Shines</h2>
    </body>
</html>
"""

                em = EmailMessage()
                em['From'] = email_sender
                em['To']= email_receiver
                em['subject']= subject
                em.set_content(MIMEText(body, 'html'))

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                


                    flash('Brand Added, and email sent to brand owner.', 'success')
                    return redirect(url_for('register_user'))
            else:
                return redirect('/register_user')
        cursor = db.connection.cursor()
        cursor.execute("select * from users")
        user_id = cursor.lastrowid
        cursor.execute("select * from brandlogo where brand_id = %s", (user_id,))
        brandlogo = cursor.fetchone()
        cursor.close()
        return render_template('dashboard/brands.html', brandlogo = brandlogo)
    else:
        return "Access denied. You must be an admin to access this page."


@app.route('/orders')
def orders():
    user_id = session.get('user_id')
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
    brandlogo = cursor.fetchone()
    user = session.get('brandname')
    return render_template('dashboard/orders.html', brandlogo=brandlogo, user = user)

@app.route('/products', methods=['GET'])
def products():
    if session.get('user_type') == 'admin':
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        
    elif session.get('user_type') == 'brandowner':
        brand = session.get('brandname')
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE brand = %s",(brand,))
        products = cursor.fetchall()
    user_id = session.get('user_id')
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
    brandlogo = cursor.fetchone()
    user = session.get('brandname')
    
    return render_template('dashboard/products.html', products = products, brandlogo=brandlogo, user=user)




@app.route('/settings')
def settings():
    return render_template('dashboard/settings.html')

@app.route('/add_product', methods=['GET'])
def add_product():
    user = session.get('brandname')
    user_id = session.get('user_id')
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
    brandlogo = cursor.fetchone()
    
    return render_template('dashboard/add_product.html', user= user, brandlogo=brandlogo)

@app.route('/upload', methods=['POST'])
def upload():
    if 'brandname' in session:
        brand = session.get('brandname')
        name = request.form['Product Name']
        image = request.files['photo']
        price = request.form['Product Price']
        description = request.form['description']
        category = request.form['category']
        type = request.form['type']

        sizes = request.form.getlist('size')

        if image:
            filename = image.filename
            cursor = db.connection.cursor()
            cursor.execute("select * from products where filename = %s", (filename,))
            file_exist = cursor.fetchone()
            if file_exist:
                flash("Product exists, if it doen't then change the filename.",'danger')
                return redirect(url_for('products'))
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
                cursor.execute("INSERT INTO products (name, price, description, type, sizes, filename, brand, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, price, description, type, ','.join(sizes), filename, brand, category))
                db.connection.commit()
                cursor.close()
                flash('Product uploaded successfully!!!', 'success')
                return redirect(url_for('products'))
    flash('Failed to upload product!','danger')
    return redirect(url_for('products'))

#Delete product on the dashboard
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if request.form.get('_method') == 'DELETE':
        cursor = db.connection.cursor()

        # Get the image path
        cursor.execute("SELECT filename FROM products WHERE id = %s", (product_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            return redirect(url_for('products'))

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], result[0])

        # Delete the product from the database
        cursor.execute("DELETE FROM reviews WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.connection.commit()

        cursor.close()

        # Delete the image file
        if os.path.exists(image_path):
            os.remove(image_path)
            return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True)