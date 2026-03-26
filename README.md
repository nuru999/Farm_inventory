🌱 Farm Inventory Management System
A modern, full-stack Farm Inventory Management System built using Flask (Python) for the backend and HTML + Tailwind CSS + JavaScript for the frontend.

This application helps manage farm inventory efficiently by allowing users to add, view, update, and delete items while providing a clean and professional dashboard interface.
🚀 Features
📊 Dashboard

Overview of inventory with real-time stats:

Total Items

Total Quantity

Total Inventory Value

📦 Inventory Management

Add new inventory items

Edit existing items

Delete items

View all inventory in a structured table

🔍 Search Functionality

Instant filtering of items based on user input

🎨 User Interface

Modern dashboard layout

Sidebar navigation

Responsive design (desktop-friendly)

Clean table UI with action buttons

Dark/Light mode toggle 🌙

🛠️ Tech Stack
Frontend

HTML5

Tailwind CSS

Vanilla JavaScript

Backend

Python

Flask

API

RESTful API endpoints:

GET /api/inventory

POST /api/inventory

PUT /api/inventory/<id>

DELETE /api/inventory/<id>

📁 Project Structure

Farm_inventory/
│
├── server/
│   ├── app.py              # Flask backend
│   ├── templates/
│   │   └── index.html      # Frontend UI
│   └── static/             # (optional assets)
│
├── README.md

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone <your-repo-url>
cd Farm_inventory
2️⃣ Install dependencies
pip install flask
3️⃣ Run the server
python app.py
4️⃣ Open in browser
http://127.0.0.1:5000
🧠 How It Works

The frontend communicates with the Flask backend using fetch()

Data is sent and received in JSON format

Inventory is dynamically rendered in the table

Actions (Edit/Delete) interact with backend API endpoints

Dashboard stats are calculated in real-time on the frontend

✨ Key Functionalities

✅ Dynamic table rendering

✅ Form handling (Add & Update)

✅ REST API integration

✅ State management using JavaScript

✅ Interactive UI (buttons, alerts, search)

🔮 Future Improvements

Authentication system (Login/Register)

Database integration (SQLite / PostgreSQL)

Export inventory (CSV/PDF)

Charts & analytics (e.g. inventory trends)

Mobile optimization

Notifications instead of alerts

👨‍💻 Author

Nuru Amudi

Aspiring Software Developer & Cybersecurity Enthusiast

📜 License

This project is open-source and free to use for learning and development purposes.
