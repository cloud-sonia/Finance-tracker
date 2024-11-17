from flask import Flask
import boto3
from flask import jsonify, render_template, request, redirect
app = Flask(__name__)
import boto3

# Create DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
dynamodb_client = boto3.client('dynamodb')
table_name = 'financeapp'

@app.route('/check_table', methods=['GET'])
def check_table():
    print("Check table route accessed")  # Debugging line
    try:
        # Use the client to describe the table
        response = dynamodb_client.describe_table(TableName=table_name)
        print("Response from DynamoDB:", response)  # Log the response
        return jsonify({
            "message": "Table exists and is accessible",
            "table_info": response
        })
    except dynamodb_client.exceptions.ResourceNotFoundException:
        print(f"Table '{table_name}' does not exist.")
        return jsonify({"message": f"Table '{table_name}' does not exist."}), 404
    except Exception as e:
        print(f"Error accessing the table: {e}")  # Log error to the terminal
        return jsonify({"error": str(e)}), 500
@app.route('/')
def home():
    return render_template('finance.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up logic here
        return redirect('/')  # Redirect to home after signup
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect('/')  # Redirect to home after login
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('financeapp')
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')  # e.g., 'us-west-2'
table = dynamodb.Table('FinanceTracker')
@app.route('/transactions/<user_id>', methods=['GET'])
def get_transactions(user_id):
    # Your logic to retrieve transactions for the specific user_id
    user_id = '12345'
    return jsonify({"user_id":  user_id})
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
    )
    return jsonify(response['Items'])
    # Check if the user exists in DynamoDB
    if 'Item' in response:
        return jsonify(response['Item'])  # Return the user transaction details as JSON
    else:
        return jsonify({'error': 'User not found'}), 404  # Return 404 if user doesn't existpyth
def home():
    return render_template('finance.html')
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.form
    user_id = '12345'
    amount = data['amount']
    category = data['category']
    transaction_date = data['transaction_date']

    table.put_item(
        Item={
            'user_id': user_id,
            'transaction_date': transaction_date,
            'amount': amount,
            'category': category
        }
    )
    return jsonify(message="Transaction added successfully")
@app.route('/usertransactions/<user_id>')
def get_user_transactions(user_id):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
    )
    return jsonify(response['Items'])
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

# Dummy data to simulate database info
users = [
    {"name": "Sarah", "savings": 10000},
    {"name": "Michael", "savings": 1500},
    {"name": "John", "savings": 2000}
]

subscribers = []

# Route for Landing Page
@app.route('/')
def index():
    # Calculate total savings
    total_savings = sum(user['savings'] for user in users)
    # Total users count
    total_users = len(users)

    return render_template('finance.html', total_users=total_users, total_savings=total_savings)

# Route for Newsletter Subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    # Check if the email is already subscribed
    if email in subscribers:
        flash("You are already subscribed!", "warning")
    else:
        subscribers.append(email)
        flash("Thank you for subscribing!", "success")

    return redirect(url_for('index'))

# Flask debug mode
if __name__ == '__main__':
    app.run(debug=True)



