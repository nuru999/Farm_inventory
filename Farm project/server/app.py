from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, InventoryModel
from flask_migrate import Migrate
from datetime import datetime
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Migrate= Migrate(app, db)
db.init_app(app)

@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json

 # Convert date strings to datetime objects
    purchase_date = datetime.strptime(data.get('purchaseDate'), '%Y-%m-%d')
    expiry_date = datetime.strptime(data.get('expiryDate'), '%Y-%m-%d')


    existing_inventory = InventoryModel.query.filter_by(
        Item=data.get('item'),
        Category=data.get('category'),
        Supplier=data.get('supplier'),
        Purchase_Date=purchase_date,
        Expiry_Date=expiry_date
    ).first()

    if existing_inventory:
        return jsonify({'error': 'Inventory already added'}), 400

    new_inventory = InventoryModel(
        Item=data.get('item'),
        Category=data.get('category'),
        Quantity=data.get('quantity'),
        Units_of_Measurement=data.get('units'),
        Unit_Cost=data.get('cost'),
        Supplier=data.get('supplier'),
        Purchase_Date=purchase_date,
        Expiry_Date=expiry_date
    )

    db.session.add(new_inventory)
    db.session.commit()

    return jsonify({'message': 'Inventory added successfully'}), 201

@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = InventoryModel.query.all()
    serialized_inventory = [{
        'Item': inv.Item,
        'Category': inv.Category,
        'Quantity': inv.Quantity,
        'Units_of_Measurement': inv.Units_of_Measurement,
        'Unit_Cost': inv.Unit_Cost,
        'Supplier': inv.Supplier,
        'Purchase_Date': inv.Purchase_Date.isoformat(),  # Convert datetime object to ISO format string
        'Expiry_Date': inv.Expiry_Date.isoformat() if inv.Expiry_Date else None  # Convert datetime object to ISO format string or None if expiry date is None
    } for inv in inventory]
    return jsonify(serialized_inventory)

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory = InventoryModel.query.get(id)
    if inventory:
        db.session.delete(inventory)
        db.session.commit()
        return jsonify({'message': 'Inventory deleted successfully'}), 200
    else:
        return jsonify({'error': 'Inventory not found'}), 404

@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_inventory(id):
    inventory = InventoryModel.query.get(id)
    if not inventory:
        return jsonify({'error': 'Inventory not found'}), 404

    data = request.json
    inventory.Item = data.get('item', inventory.Item)
    inventory.Category = data.get('category', inventory.Category)
    inventory.Quantity = data.get('quantity', inventory.Quantity)
    inventory.Units_of_Measurement = data.get('units', inventory.Units_of_Measurement)
    inventory.Unit_Cost = data.get('cost', inventory.Unit_Cost)
    inventory.Supplier = data.get('supplier', inventory.Supplier)

    # Convert date strings to Python datetime objects
    purchase_date_str = data.get('purchaseDate')
    if purchase_date_str:
        inventory.Purchase_Date = datetime.strptime(purchase_date_str, '%Y-%m-%d')

    expiry_date_str = data.get('expiryDate')
    if expiry_date_str:
        inventory.Expiry_Date = datetime.strptime(expiry_date_str, '%Y-%m-%d')

    db.session.commit()
    return jsonify({'message': 'Inventory updated successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)
