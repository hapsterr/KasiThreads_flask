import random
import re
import smtplib
import ssl
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from models import kasithreads_db
import bcrypt
import os
from email.message import EmailMessage

email_sender = 'happyseoketsa@gmail.com'
email_password = 'sstu ypai kfrz cgio'
customer_verification_code = None 

app = Flask(__name__)
db = kasithreads_db(app)
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
    cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
    product = cursor.fetchone()
    db.connection.commit()
    cursor.close()
    if product:
        sizes = product[5].split(',') if product[5] else []
        return render_template('website/product.html', product=product, sizes=sizes)
    else:
        return "Product not found"
    

@app.route('/account')
def account():
    return render_template('website/login.html')



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
                body = """USE THIS CODE TO VERIFY YOUR KASITHREADS ACCOUNT: """+ str(customer_verification_code)

                em = EmailMessage()
                em['From'] = email_sender
                em['To']= email_receiver
                em['subject']= subject
                em.set_content(body)

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
@app.route('/forgot_password')
def forgot_password():
    return render_template('website/forgot_password.html')

@app.route('/about')
def about():
    return render_template('website/about.html')


@app.route('/cart')
def cart():
    return render_template('website/cart.html')

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
@app.route('/register_user', methods=['POST'])
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
                return 'Brand successfully Added'
            else:
                return redirect('/register_user')
        return render_template('dashboard/brands.html')
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
        type = request.form['type']
        sizes = request.form.getlist('size')

        if image:
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO products (name, price, description, type, sizes, filename, brand) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, price, description, type, ','.join(sizes), filename, brand))
            db.connection.commit()
            cursor.close()
            return 'Product uploaded successfully!'
    return 'Failed to upload product!'

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
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.connection.commit()

        cursor.close()

        # Delete the image file
        if os.path.exists(image_path):
            os.remove(image_path)
            return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True)