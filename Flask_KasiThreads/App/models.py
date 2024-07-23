# This file handles database operations

from flask_mysqldb import MySQL

def kasithreads_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '0735032076Akukho'
    app.config['MYSQL_DB'] = 'kasithreads_db'

    mysql = MySQL(app)
    return mysql

