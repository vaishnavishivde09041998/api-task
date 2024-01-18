from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for simplicity. In a real-world application, use a proper database.
train_data = {
    'users': [],
    'seats': {
        'A': [],
        'B': []
    }
}

@app.route('/purchase_ticket', methods=['POST'])
def purchase_ticket():
    data = request.get_json()

    user = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    }

    price_paid = 20
    user['price_paid'] = price_paid

    # Assume a simple seat allocation logic: alternate between sections A and B
    section = 'A' if len(train_data['seats']['A']) <= len(train_data['seats']['B']) else 'B'
    seat_number = len(train_data['seats'][section]) + 1
    user['section'] = section
    user['seat_number'] = seat_number

    train_data['users'].append(user)
    train_data['seats'][section].append(user)

    receipt = {
        'From': 'London',
        'To': 'France',
        'User': user,
        'price_paid': price_paid
    }

    return jsonify(receipt)

@app.route('/view_receipt/<int:user_id>', methods=['GET'])
def view_receipt(user_id):
    if user_id < 1 or user_id > len(train_data['users']):
        return jsonify({'error': 'User not found'})

    user = train_data['users'][user_id - 1]
    receipt = {
        'From': 'London',
        'To': 'France',
        'User': user,
        'price_paid': user['price_paid']
    }

    return jsonify(receipt)

@app.route('/view_users_by_section/<string:section>', methods=['GET'])
def view_users_by_section(section):
    if section not in train_data['seats']:
        return jsonify({'error': 'Invalid section'})

    users_in_section = train_data['seats'][section]
    return jsonify(users_in_section)

@app.route('/remove_user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    if user_id < 1 or user_id > len(train_data['users']):
        return jsonify({'error': 'User not found'})

    user = train_data['users'].pop(user_id - 1)
    train_data['seats'][user['section']].remove(user)

    return jsonify({'message': 'User removed successfully'})

@app.route('/modify_seat/<int:user_id>', methods=['PUT'])
def modify_seat(user_id):
    if user_id < 1 or user_id > len(train_data['users']):
        return jsonify({'error': 'User not found'})

    user = train_data['users'][user_id - 1]
    current_section = user['section']
    current_seat_number = user['seat_number']

    # Change section (toggle between A and B)
    new_section = 'A' if current_section == 'B' else 'B'
    user['section'] = new_section

    # Keep the same seat number for simplicity, but you can implement more complex logic
    train_data['seats'][current_section].remove(user)
    train_data['seats'][new_section].append(user)

    return jsonify({'message': 'Seat modified successfully'})

if __name__ == '__main__':
    app.run(debug=True)
