from flask import Flask, jsonify, request, abort, url_for

app = Flask(__name__)

# Sample data - list of persons
persons = [
    {
        "id": 1, 
        "name": "John Doe", 
        "address": "123 Main St", 
        "phone_number": "34567890", 
        "personnummer": "12345678901", 
        "account_balance": 1000.00
    },
    {
        "id": 2, 
        "name": "Jane Smith", 
        "address": "456 Elm St", 
        "phone_number": "87654321", 
        "personnummer": "10987654321", 
        "account_balance": 1500.00
    }
]

def make_public_person(person):
    """
    Modify the person to add HATEOAS links.
    This helps in providing hypermedia-driven navigation to the client.
    """
    new_person = {}
    for field in person:
        if field == 'id':
            new_person['uri'] = url_for('get_person', person_id=person['id'], _external=True)
            new_person['links'] = [
                {"rel": "self", "href": new_person['uri']},
                {"rel": "update", "href": new_person['uri'], "method": "PUT"},
                {"rel": "delete", "href": new_person['uri'], "method": "DELETE"}
            ]
        else:
            new_person[field] = person[field]
    return new_person

@app.route('/persons', methods=['GET'])
def get_persons():
    """
    Endpoint to get a list of all persons.
    Returns a JSON array of persons with HATEOAS links.
    """
    return jsonify([make_public_person(person) for person in persons])

@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    """
    Endpoint to get a specific person by ID.
    Returns a single person object in JSON format if found, else 404.
    """
    person = next((person for person in persons if person['id'] == person_id), None)
    if person:
        return jsonify(make_public_person(person))
    else:
        abort(404)

@app.route('/persons', methods=['POST'])
def create_person():
    """
    Endpoint to add a new person.
    Expects a JSON object with person's details.
    Returns the created person object with a 201 status code.
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    person = {
        'id': persons[-1]['id'] + 1 if persons else 1,
        'name': request.json['name'],
        'address': request.json['address'],
        'phone_number': request.json['phone_number'],
        'personnummer': request.json['personnummer'],
        'account_balance': request.json['account_balance']
    }
    persons.append(person)
    return jsonify(make_public_person(person)), 201

@app.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    """
    Endpoint to update an existing person's details.
    Expects a JSON object with person's new details.
    Returns the updated person object if found, else 404.
    """
    person = next((person for person in persons if person['id'] == person_id), None)
    if not person:
        abort(404)
    if not request.json:
        abort(400)
    person['name'] = request.json.get('name', person['name'])
    person['address'] = request.json.get('address', person['address'])
    person['phone_number'] = request.json.get('phone_number', person['phone_number'])
    person['personnummer'] = request.json.get('personnummer', person['personnummer'])
    person['account_balance'] = request.json.get('account_balance', person['account_balance'])
    return jsonify(make_public_person(person))

@app.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """
    Endpoint to delete a person by ID.
    Returns a JSON object with the result of the operation.
    """
    global persons
    persons = [person for person in persons if person['id'] != person_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
