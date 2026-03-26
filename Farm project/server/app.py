from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from models import db, InventoryModel

app = Flask(__name__)

# CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# =======================
# HELPER FUNCTION
# =======================
def serialize_item(inv):
    return {
        'id': inv.id,
        'Item': inv.Item,
        'Category': inv.Category,
        'Quantity': inv.Quantity,
        'Units_of_Measurement': inv.Units_of_Measurement,
        'Unit_Cost': inv.Unit_Cost,
        'Supplier': inv.Supplier,
        'Purchase_Date': inv.Purchase_Date.strftime('%Y-%m-%d') if inv.Purchase_Date else None,
        'Expiry_Date': inv.Expiry_Date.strftime('%Y-%m-%d') if inv.Expiry_Date else None
    }

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
    return jsonify([serialize_item(inv) for inv in inventories])

# =======================
# ADD INVENTORY
# =======================
@app.route('/api/inventory', methods=['POST'])
def api_add_inventory():
    data = request.get_json()

    try:
        purchase_date = datetime.strptime(data.get('Purchase_Date'), '%Y-%m-%d') if data.get('Purchase_Date') else None
        expiry_date = datetime.strptime(data.get('Expiry_Date'), '%Y-%m-%d') if data.get('Expiry_Date') else None

        new_item = InventoryModel(
            Item=data.get('Item'),
            Category=data.get('Category'),
            Quantity=int(data.get('Quantity', 0)),
            Units_of_Measurement=data.get('Units_of_Measurement'),
            Unit_Cost=float(data.get('Unit_Cost', 0)),
            Supplier=data.get('Supplier'),
            Purchase_Date=purchase_date,
            Expiry_Date=expiry_date
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Item added successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# =======================
# DELETE INVENTORY
# =======================
@app.route('/api/inventory/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = InventoryModel.query.get(id)

    if not item:
        return jsonify({
            "status": "error",
            "message": "Item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Item deleted successfully"
    })

# =======================
# UPDATE INVENTORY
# =======================
@app.route('/api/inventory/<int:id>', methods=['PUT'])
def update_item(id):
    item = InventoryModel.query.get(id)

    if not item:
        return jsonify({
            "status": "error",
            "message": "Item not found"
        }), 404

    data = request.get_json()

    try:
        item.Item = data.get('Item', item.Item)
        item.Category = data.get('Category', item.Category)
        item.Quantity = int(data.get('Quantity', item.Quantity))
        item.Units_of_Measurement = data.get('Units_of_Measurement', item.Units_of_Measurement)
        item.Unit_Cost = float(data.get('Unit_Cost', item.Unit_Cost))
        item.Supplier = data.get('Supplier', item.Supplier)

        if data.get('Purchase_Date'):
            item.Purchase_Date = datetime.strptime(data.get('Purchase_Date'), '%Y-%m-%d')

        if data.get('Expiry_Date'):
            item.Expiry_Date = datetime.strptime(data.get('Expiry_Date'), '%Y-%m-%d')

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Item updated successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# =======================
# RUN APP
# =======================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)