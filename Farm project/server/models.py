from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InventoryModel(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    Item = db.Column(db.String(20), nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Units_of_Measurement = db.Column(db.String(15), nullable=False)
    Unit_Cost = db.Column(db.Integer, nullable=False)
    Supplier = db.Column(db.String(50), nullable=False)
    Purchase_Date = db.Column(db.DateTime)
    Expiry_Date = db.Column(db.DateTime)

    # def __repr__(self):
    #     return f'<InventoryModel {self.Item}>'

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'item': self.Item,
    #         'category': self.Category,
    #         'quantity': self.Quantity,
    #         'units': self.Units_of_Measurement,
    #         'cost': self.Unit_Cost,
    #         'supplier': self.Supplier,
    #         'purchaseDate': self.Purchase_Date,
    #         'expiryDate': self.Expiry_Date
    #     }
