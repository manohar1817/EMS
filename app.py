from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="testdb"
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


# User Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    try:
        # Connect to MySQL
        cur = mysql.connection.cursor()
        
        # Insert into users table
        cur.execute("""
            INSERT INTO users (
                username, email, password, mobile_number, role, 
                region, address, city, state, zipcode, particular_mark
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['username'], data['email'], data['password'], data['mobile_number'], data['role'],
            data['region'], data['address'], data['city'], data['state'], data['zipcode'], data['mark']
        ))
        
        # Get the inserted user_id
        user_id = cur.lastrowid
        
        # Insert into user_statistics table
        cur.execute("""
            INSERT INTO user_statistics (user_id) VALUES (%s)
        """, (user_id,))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'success': True,
            'redirect': 'NGO.html' if data['role'] == 'NGO' else 'RestaurantCaterer.html'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Login Endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT * FROM users 
            WHERE email = %s AND password = %s AND role = %s
        """, (data['email'], data['password'], data['role']))
        
        user = cur.fetchone()
        cur.close()
        
        if user:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user['user_id'],
                    'username': user['username'],
                    'role': user['role'],
                    'email': user['email']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Create Donation Endpoint
@app.route('/api/create_donation', methods=['POST'])
def create_donation():
    data = request.json
    
    try:
        cur = mysql.connection.cursor()
        
        # Get user_id from session (you'll need to implement session management)
        user_id = 1  # This should come from the authenticated session
        
        cur.execute("""
            INSERT INTO donations (
                donor_id, quantity, food_type, cooked_time, expiry_hours,
                hygiene_rating, status, address, city, state, zipcode, particular_mark
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, data['quantity'], data['food_type'], data['cooked_time'], data['expiry_hours'],
            data['hygiene_rating'], 'Available', data['address'], data['city'], 
            data['state'], data['zipcode'], data['mark']
        ))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)