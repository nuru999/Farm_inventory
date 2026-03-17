from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from models import db, InventoryModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# =======================
# HOME PAGE
# =======================
@app.route('/')
def home():
    return render_template('index.html')


# =======================
# GET ALL INVENTORY
# =======================
@app.route('/api/inventory', methods=['GET'])
def api_get_inventory():
    inventories = InventoryModel.query.all()
    result = []

    for inv in inventories:
        result.append({
            'id': inv.id,
            'Item': inv.Item,
            'Category': inv.Category,
            'Quantity': inv.Quantity,
            'Units_of_Measurement': inv.Units_of_Measurement,
            'Unit_Cost': inv.Unit_Cost,
            'Supplier': inv.Supplier,
            'Purchase_Date': inv.Purchase_Date.strftime('%Y-%m-%d') if inv.Purchase_Date else None,
            'Expiry_Date': inv.Expiry_Date.strftime('%Y-%m-%d') if inv.Expiry_Date else None
        })

    return jsonify(result)


# =======================
# ADD INVENTORY (POST)
# =======================
@app.route('/api/inventory', methods=['POST'])
def api_add_inventory():
    data = request.json

    try:
        purchase_date = datetime.strptime(data.get('Purchase_Date'), '%Y-%m-%d')
        expiry_date = datetime.strptime(data.get('Expiry_Date'), '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    new_inventory = InventoryModel(
        Item=data.get('Item'),
        Category=data.get('Category'),
        Supplier=data.get('Supplier'),
        Purchase_Date=purchase_date,
        Expiry_Date=expiry_date,
        Quantity=data.get('Quantity'),
        Units_of_Measurement=data.get('Units_of_Measurement'),
        Unit_Cost=data.get('Unit_Cost')
    )

    db.session.add(new_inventory)
    db.session.commit()

    return jsonify({"message": "Inventory added successfully"})


# =======================
# DELETE INVENTORY
# =======================
@app.route('/api/inventory/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = InventoryModel.query.get(id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted successfully"})


# =======================
# UPDATE INVENTORY (PUT)
# =======================
@app.route('/api/inventory/<int:id>', methods=['PUT'])
def update_item(id):
    item = InventoryModel.query.get(id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    item.Item = data.get('Item', item.Item)
    item.Category = data.get('Category', item.Category)
    item.Quantity = data.get('Quantity', item.Quantity)
    item.Units_of_Measurement = data.get('Units_of_Measurement', item.Units_of_Measurement)
    item.Unit_Cost = data.get('Unit_Cost', item.Unit_Cost)
    item.Supplier = data.get('Supplier', item.Supplier)

    # FIX: convert dates properly
    if data.get('Purchase_Date'):
        item.Purchase_Date = datetime.strptime(data.get('Purchase_Date'), '%Y-%m-%d')

    if data.get('Expiry_Date'):
        item.Expiry_Date = datetime.strptime(data.get('Expiry_Date'), '%Y-%m-%d')

    db.session.commit()

    return jsonify({"message": "Item updated successfully"})


# =======================
# RUN APP
# =======================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)