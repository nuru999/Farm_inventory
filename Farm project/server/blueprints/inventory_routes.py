from flask import jsonify, request
from datetime import datetime
from models import db, InventoryModel
from . import inventory_bp

# =======================
# VALIDATION HELPERS
# =======================

def validate_inventory_data(data):
    """Validate inventory item data"""
    errors = []
    
    if not data.get('Item'):
        errors.append('Item name is required')
    
    if not data.get('Category'):
        errors.append('Category is required')
    
    try:
        qty = int(data.get('Quantity', 0))
        if qty < 0:
            errors.append('Quantity cannot be negative')
    except (ValueError, TypeError):
        errors.append('Quantity must be a number')
    
    try:
        cost = float(data.get('Unit_Cost', 0))
        if cost < 0:
            errors.append('Unit cost cannot be negative')
    except (ValueError, TypeError):
        errors.append('Unit cost must be a number')
    
    if not data.get('Supplier'):
        errors.append('Supplier is required')
    
    if not data.get('Units_of_Measurement'):
        errors.append('Units of measurement is required')
    
    return errors


def parse_date(date_str):
    """Parse date string safely"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None


def serialize_item(item):
    """Convert model to dictionary"""
    return {
        'id': item.id,
        'Item': item.Item,
        'Category': item.Category,
        'Quantity': item.Quantity,
        'Units_of_Measurement': item.Units_of_Measurement,
        'Unit_Cost': float(item.Unit_Cost),
        'Supplier': item.Supplier,
        'Purchase_Date': item.Purchase_Date.strftime('%Y-%m-%d') if item.Purchase_Date else None,
        'Expiry_Date': item.Expiry_Date.strftime('%Y-%m-%d') if item.Expiry_Date else None,
        'created_at': item.created_at.isoformat() if item.created_at else None,
        'updated_at': item.updated_at.isoformat() if item.updated_at else None
    }


# =======================
# GET ROUTES
# =======================

@inventory_bp.route('/inventory', methods=['GET'])
def get_all_inventory():
    """Get all inventory items with optional filtering"""
    try:
        # Optional: Add filtering
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = InventoryModel.query
        
        if category:
            query = query.filter_by(Category=category)
        
        if search:
            query = query.filter(InventoryModel.Item.ilike(f'%{search}%'))
        
        items = query.all()
        
        return jsonify({
            'status': 'success',
            'data': [serialize_item(item) for item in items],
            'count': len(items)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch inventory: {str(e)}'
        }), 500


@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get single inventory item"""
    try:
        item = InventoryModel.query.get(item_id)
        
        if not item:
            return jsonify({
                'status': 'error',
                'message': 'Item not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': serialize_item(item)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory/stats', methods=['GET'])
def get_stats():
    """Get inventory statistics"""
    try:
        items = InventoryModel.query.all()
        
        total_items = len(items)
        total_quantity = sum(item.Quantity for item in items)
        total_value = sum((item.Quantity * item.Unit_Cost) for item in items)
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_items': total_items,
                'total_quantity': total_quantity,
                'total_value': float(total_value),
                'average_cost': float(total_value / total_items) if total_items > 0 else 0
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# =======================
# POST ROUTES
# =======================

@inventory_bp.route('/inventory', methods=['POST'])
def create_item():
    """Create new inventory item"""
    try:
        data = request.get_json()
        
        # Validate input
        validation_errors = validate_inventory_data(data)
        if validation_errors:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'errors': validation_errors
            }), 400
        
        # Create item
        new_item = InventoryModel(
            Item=data.get('Item').strip(),
            Category=data.get('Category').strip(),
            Quantity=int(data.get('Quantity', 0)),
            Units_of_Measurement=data.get('Units_of_Measurement').strip(),
            Unit_Cost=float(data.get('Unit_Cost', 0)),
            Supplier=data.get('Supplier').strip(),
            Purchase_Date=parse_date(data.get('Purchase_Date')),
            Expiry_Date=parse_date(data.get('Expiry_Date'))
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'data': serialize_item(new_item)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to create item: {str(e)}'
        }), 500


# =======================
# PUT ROUTES
# =======================

@inventory_bp.route('/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update inventory item"""
    try:
        item = InventoryModel.query.get(item_id)
        
        if not item:
            return jsonify({
                'status': 'error',
                'message': 'Item not found'
            }), 404
        
        data = request.get_json()
        
        # Validate input if provided
        if any(key in data for key in ['Item', 'Category', 'Quantity', 'Unit_Cost', 'Supplier', 'Units_of_Measurement']):
            validation_errors = validate_inventory_data(data)
            if validation_errors:
                return jsonify({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': validation_errors
                }), 400
        
        # Update fields
        item.Item = data.get('Item', item.Item).strip() if data.get('Item') else item.Item
        item.Category = data.get('Category', item.Category).strip() if data.get('Category') else item.Category
        item.Quantity = int(data.get('Quantity', item.Quantity))
        item.Units_of_Measurement = data.get('Units_of_Measurement', item.Units_of_Measurement).strip() if data.get('Units_of_Measurement') else item.Units_of_Measurement
        item.Unit_Cost = float(data.get('Unit_Cost', item.Unit_Cost))
        item.Supplier = data.get('Supplier', item.Supplier).strip() if data.get('Supplier') else item.Supplier
        
        if data.get('Purchase_Date'):
            item.Purchase_Date = parse_date(data.get('Purchase_Date'))
        
        if data.get('Expiry_Date'):
            item.Expiry_Date = parse_date(data.get('Expiry_Date'))
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Item updated successfully',
            'data': serialize_item(item)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update item: {str(e)}'
        }), 500


# =======================
# DELETE ROUTES
# =======================

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete inventory item"""
    try:
        item = InventoryModel.query.get(item_id)
        
        if not item:
            return jsonify({
                'status': 'error',
                'message': 'Item not found'
            }), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Item deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete item: {str(e)}'
        }), 500
