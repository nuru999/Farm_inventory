from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class InventoryModel(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)

    Item = db.Column(db.String(100), nullable=False)
    Category = db.Column(db.String(100), nullable=False)

    Quantity = db.Column(db.Integer, nullable=False, default=0)
    Units_of_Measurement = db.Column(db.String(50), nullable=False)

    Unit_Cost = db.Column(db.Float, nullable=False, default=0.0)

    Supplier = db.Column(db.String(100), nullable=False)

    Purchase_Date = db.Column(db.DateTime, nullable=True)
    Expiry_Date = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'Item': self.Item,
            'Category': self.Category,
            'Quantity': self.Quantity,
            'Units_of_Measurement': self.Units_of_Measurement,
            'Unit_Cost': self.Unit_Cost,
            'Supplier': self.Supplier,
            'Purchase_Date': self.Purchase_Date.strftime('%Y-%m-%d') if self.Purchase_Date else None,
            'Expiry_Date': self.Expiry_Date.strftime('%Y-%m-%d') if self.Expiry_Date else None
        }