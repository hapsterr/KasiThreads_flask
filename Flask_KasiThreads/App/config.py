from flask import Flask, jsonify, redirect, render_template, request, session, url_for
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
    return render_template('website/home.html')


#Sort By
@app.route('/shop', methods=['GET'])
def shop():
    sort_by = request.args.get('sort_by', 'name')  # Default sort by name
    
    cursor = db.connection.cursor()

    if sort_by == 'price_asc':
        query = "SELECT * FROM products ORDER BY price ASC"
    elif sort_by == 'price_desc':
        query = "SELECT * FROM products ORDER BY price DESC"
    elif sort_by == 'title_desc':
        query = "SELECT * FROM products ORDER BY name DESC"
    elif sort_by == 'title_asc':
        query = "SELECT * FROM products ORDER BY name ASC"
    else:
        query = "SELECT * FROM products ORDER BY name"

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()

    return render_template('website/shop.html', products=products)

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

@app.route('/home')
def home():
    if 'brandname' in session:
        user = session.get('brandname')
        user_type = session.get('user_type')
        return render_template('dashboard/home.html', user =user, user_type = user_type)
    else:
        return "Access denied. You must be logged in to access this page."


@app.route('/home_photos')
def home_photos():
   return render_template('dashboard/home_photos.html')
    

@app.route('/brands')
def brands():
    if session.get('user_type') == 'admin':
        return render_template('dashboard/brands.html')
    else:
        # Redirect to a different page or show an error message.
        return "Access denied. You must be an admin to access this page."

#Adding users into the dashboard
@app.route('/register_user', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        brandname = request.form['brandname']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO users (brandname, email, password, user_type) VALUES (%s, %s, %s, %s)", (brandname, email, hashed_password, user_type))
        db.connection.commit()
        cursor.close()
        return redirect('/register_user')
    return render_template('dashboard/brands.html')

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

@app.route('/orders')
def orders():
    return render_template('dashboard/orders.html')

@app.route('/products', methods=['GET'])
def products():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('dashboard/products.html', products = products)



@app.route('/settings')
def settings():
    return render_template('dashboard/settings.html')

@app.route('/add_product', methods=['GET'])
def add_product():
    return render_template('dashboard/add_product.html')

@app.route('/upload', methods=['POST'])
def upload():
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
        cursor.execute("INSERT INTO products (name, price, description, type, sizes, filename) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, description, type, ','.join(sizes), filename))
        db.connection.commit()
        cursor.close()
        return 'Product uploaded successfully!'
    return 'Failed to upload product!'


@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # Connect to the database
        
        cursor = db.connection.cursor()

        # Get the image path
        cursor.execute("SELECT image_path FROM products WHERE id = %s", (product_id))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Product not found'}), 404

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], result[3])

        # Delete the product from the database
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id))
        db.connection.commit()

        # Close the database connection
        cursor.close()
        db.connection.close()

        # Delete the image file
        if os.path.exists(image_path):
            os.remove(image_path)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)