# 🌱 Farm Inventory Management System - Enhanced Edition

A production-ready **full-stack** Farm Inventory Management System built with **Flask** (Python backend) and **HTML + Tailwind CSS + JavaScript** (frontend), featuring **PostgreSQL** database support for scalable deployments.

## ✨ Features

### Core Features
- 📊 **Dashboard Overview** - Real-time inventory statistics
  - Total items count
  - Total quantity in stock
  - Inventory value calculation
  - Average cost metrics

- 📦 **Inventory Management**
  - Add new items with validation
  - Edit existing items
  - Delete items with confirmation
  - Search and filter functionality

- 🔍 **Advanced Search**
  - Real-time filtering by name
  - Category-based filtering
  - Multiple search criteria

- 💾 **Data Persistence**
  - SQLite (development)
  - PostgreSQL (production)
  - Automatic migrations

### Technical Features
- ✅ **RESTful API** - Clean, documented endpoints
- ✅ **Input Validation** - Server-side validation for all inputs
- ✅ **Error Handling** - Comprehensive error messages
- ✅ **CORS Support** - Cross-origin resource sharing enabled
- ✅ **Database Blueprints** - Modular Flask application structure
- ✅ **Environment Configuration** - Development, production, testing configs
- ✅ **Migration Support** - Alembic for database schema management

## 🚀 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.0 + Flask-SQLAlchemy |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **ORM** | SQLAlchemy |
| **Migrations** | Alembic + Flask-Migrate |
| **API** | RESTful with JSON |
| **Server** | Gunicorn (production) |

## 📁 Project Structure

```
Farm_inventory/
├── Farm project/
│   └── server/
│       ├── app-improved.py                 # Main Flask app (refactored)
│       ├── config.py                       # Configuration management (NEW)
│       ├── models.py                       # SQLAlchemy models
│       ├── requirements.txt                # Python dependencies (NEW)
│       ├── .env.example                    # Environment template (NEW)
│       ├── blueprints/                     # Modular routes (NEW)
│       │   ├── __init__.py                # Blueprint initialization
│       │   └── inventory_routes.py        # API endpoints
│       ├── migrations/                     # Database migrations
│       ├── templates/                      # HTML files
│       │   ├── dashboard.html
│       │   ├── inventory.html
│       │   └── settings.html
│       └── instance/                       # Database file (created at runtime)
├── README.md
└── README-IMPROVED.md                      # This file
```

## 🔧 Setup & Installation

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+ (optional, for production)
- pip or pipenv
- Virtual environment support

### 2. Clone & Navigate
```bash
cd Farm_inventory/"Farm project"/server
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment

**Development (SQLite)**:
```bash
cp .env.example .env.local
# No changes needed, uses SQLite by default
```

**Production (PostgreSQL)**:
```bash
cp .env.example .env.local
# Edit .env.local and add:
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/farm_inventory_db
SECRET_KEY=your-secure-secret-key
```

### 6. Initialize Database

```bash
# Create tables
export FLASK_APP=app-improved.py
flask db init              # First time only
flask db migrate           # Create migration
flask db upgrade           # Apply migration

# Or use CLI command:
flask init-db
flask seed-db              # Optional: Load sample data
```

### 7. Run Application

**Development**:
```bash
python app-improved.py
# Server runs at http://127.0.0.1:5000
```

**Production** (using Gunicorn):
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app-improved.py
```

## 📖 How It Works

### Architecture
```
┌──────────────────────────────────────┐
│      Browser / Frontend              │
│   (HTML + Tailwind + Vanilla JS)     │
└──────────────┬───────────────────────┘
               │ HTTP/JSON
┌──────────────▼───────────────────────┐
│      Flask Application               │
├──────────────────────────────────────┤
│  Pages Blueprint                     │
│  ├─ GET / → dashboard.html           │
│  ├─ GET /inventory → inventory.html  │
│  └─ GET /settings → settings.html    │
├──────────────────────────────────────┤
│  Inventory Blueprint                 │
│  ├─ GET /api/inventory → list items  │
│  ├─ POST /api/inventory → create     │
│  ├─ PUT /api/inventory/id → update   │
│  └─ DELETE /api/inventory/id → delete│
├──────────────────────────────────────┤
│  Models (SQLAlchemy)                 │
│  └─ InventoryModel                   │
└──────────────┬───────────────────────┘
               │ SQL
┌──────────────▼───────────────────────┐
│   Database                           │
│   SQLite (dev) | PostgreSQL (prod)   │
└──────────────────────────────────────┘
```

### Data Flow

**Create Item**:
```
User Form Submit
    ↓
POST /api/inventory (JSON)
    ↓
Blueprint Route Handler
    ↓
Data Validation
    ↓
SQLAlchemy Model Create
    ↓
Database Insert
    ↓
JSON Response (201 Created)
    ↓
JavaScript Updates DOM
```

**Update Item**:
```
User Edit Form
    ↓
PUT /api/inventory/<id> (JSON)
    ↓
Find Item in DB
    ↓
Validate New Data
    ↓
Update Fields
    ↓
Database Commit
    ↓
JSON Response (200 OK)
    ↓
DOM Updates
```

### Database Schema

```sql
CREATE TABLE inventories (
  id INTEGER PRIMARY KEY,
  Item VARCHAR(100) NOT NULL,
  Category VARCHAR(100) NOT NULL,
  Quantity INTEGER NOT NULL DEFAULT 0,
  Units_of_Measurement VARCHAR(50) NOT NULL,
  Unit_Cost FLOAT NOT NULL DEFAULT 0.0,
  Supplier VARCHAR(100) NOT NULL,
  Purchase_Date DATETIME,
  Expiry_Date DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Get All Items
```http
GET /api/inventory
Response:
{
  "status": "success",
  "data": [...],
  "count": 10
}
```

#### Get Single Item
```http
GET /api/inventory/<id>
Response:
{
  "status": "success",
  "data": {...}
}
```

#### Create Item
```http
POST /api/inventory
Content-Type: application/json

{
  "Item": "Maize Seeds",
  "Category": "Seeds",
  "Quantity": 100,
  "Units_of_Measurement": "kg",
  "Unit_Cost": 5.50,
  "Supplier": "AgriSupply Co.",
  "Purchase_Date": "2024-05-01",
  "Expiry_Date": "2025-05-01"
}

Response: 201 Created
```

#### Update Item
```http
PUT /api/inventory/<id>
Content-Type: application/json

{
  "Quantity": 150,
  "Unit_Cost": 6.00
}

Response: 200 OK
```

#### Delete Item
```http
DELETE /api/inventory/<id>
Response: 200 OK
```

#### Get Statistics
```http
GET /api/inventory/stats
Response:
{
  "status": "success",
  "stats": {
    "total_items": 15,
    "total_quantity": 1500,
    "total_value": 12500.00,
    "average_cost": 833.33
  }
}
```

### Filtering & Search

```http
GET /api/inventory?category=Seeds
GET /api/inventory?search=Maize
GET /api/inventory?category=Equipment&search=Pipe
```

## 🔐 Security & Best Practices

✅ **Input Validation**
- Server-side validation on all endpoints
- Type checking (int, float, string)
- Required field verification
- Date format validation

✅ **Error Handling**
- Specific error messages
- HTTP status codes (201, 400, 404, 500)
- Database rollback on errors
- Try-catch blocks around all operations

✅ **Data Protection**
- CORS enabled for specific origins
- Session management
- Database transaction integrity
- SQL injection prevention (SQLAlchemy ORM)

✅ **Configuration Management**
- Environment variables via .env
- Separate dev/prod configs
- Secret key for sessions
- No hardcoded credentials

✅ **Performance**
- Efficient queries
- Database indexing (on ID, Category)
- Pagination ready
- Optimized JSON serialization

## 📊 Model Schema

```python
class InventoryModel(db.Model):
    id: int                           # Primary key
    Item: str (100)                   # Item name (required)
    Category: str (100)               # Category (required)
    Quantity: int                     # Stock quantity (required)
    Units_of_Measurement: str (50)    # Unit type (required)
    Unit_Cost: float                  # Price per unit (required)
    Supplier: str (100)               # Supplier name (required)
    Purchase_Date: datetime           # When purchased (optional)
    Expiry_Date: datetime             # Expiration date (optional)
    created_at: datetime              # Record creation time
    updated_at: datetime              # Last update time
```

## 🚀 Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app-improved.py
```

### Using Docker
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app-improved.py"]
```

### PostgreSQL Setup
```bash
# Create database
createdb farm_inventory_db

# Create user
createuser farm_user
# Set password when prompted

# Grant privileges
psql -d farm_inventory_db -c "GRANT ALL PRIVILEGES ON SCHEMA public TO farm_user;"
```

## 🐛 Troubleshooting

### "Database does not exist" error
**Solution**:
```bash
flask db upgrade
flask init-db
```

### "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```bash
pip install -r requirements.txt
```

### "Port 5000 already in use"
**Solution**:
```bash
python app-improved.py --port 5001
# Or kill the process using port 5000
```

### PostgreSQL connection error
**Solution**:
1. Verify PostgreSQL is running
2. Check DATABASE_URL in .env.local
3. Verify username and password
4. Check database exists: `psql -l`

## 📈 Future Enhancements

- [ ] User authentication & authorization
- [ ] Role-based access control (Admin, Staff)
- [ ] Advanced reporting & analytics
- [ ] CSV import/export functionality
- [ ] Barcode scanning support
- [ ] Mobile app (React Native)
- [ ] Real-time inventory updates (WebSocket)
- [ ] Automated low-stock alerts
- [ ] Supplier management system
- [ ] Multi-farm support
- [ ] Batch operations
- [ ] Audit logging
- [ ] Data backup automation

## 📜 License

Open source. Free to use for learning and development.

---

**Last Updated**: May 7, 2024
**Version**: 2.0 (Enhanced with PostgreSQL & Blueprints)
**Database Independence**: ✅ Verified (No external dependencies)
