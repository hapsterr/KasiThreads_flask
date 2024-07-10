from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from models import kasithreads_db
import bcrypt
import os

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
    cursor.close()
    return render_template('website/home.html', brands =brands, products =products)


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

    cursor.close()

    return render_template('website/shop.html', products=products)

# Product Details
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
    product = cursor.fetchone()
    
    if product:
        sizes = product[5].split(',') if product[5] else []
        return render_template('website/product.html', product=product, sizes=sizes)
    else:
        return "Product not found", 404
@app.route('/account')
def account():
    return render_template('website/login.html')

@app.route('/register')
def register():
    return render_template('website/register.html')

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
            return  redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again."
    
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
        return render_template("dashboard/home_photos.html", brandlogo=brandlogo)
    else:
        flash("Access denied. You must be an admin to access this page.", 'danger')
        return redirect(url_for('home'))
    

@app.route('/brands')
def brands():
    if session.get('user_type') == 'admin':
        user = session.get('brandname')
        user_id = session.get('user_id')
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM brandlogo WHERE brand_id = %s", (user_id,))
        brandlogo = cursor.fetchone()
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


@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cursor = db.connection.cursor()

        # Get the image path
        cursor.execute("SELECT image_path FROM products WHERE id = %s", (product_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            return jsonify({'error': 'Product not found'}), 404

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], result[0])

        # Delete the product from the database
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.connection.commit()

        cursor.close()

        # Delete the image file
        if os.path.exists(image_path):
            os.remove(image_path)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)