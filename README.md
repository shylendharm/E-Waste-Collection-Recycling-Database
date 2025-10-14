# E-Waste Collection & Recycling System

A web application to manage e-waste collection records in colleges and organizations.

## Features

- Add new e-waste collection records
- View all collection records in a tabular format
- Update collection status (Pending/Collected)
- Delete records when necessary
- Generate reports on e-waste collection
- Clean and responsive web interface

## Technology Stack

- Backend: Python with Flask
- Database: SQLite3
- Frontend: HTML, CSS, JavaScript

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python backend/app.py`
4. Access the application at `http://localhost:5000`

## Database Schema

### users table
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- name: TEXT
- email: TEXT (UNIQUE)
- password: TEXT

### ewaste_records table
- record_id: INTEGER PRIMARY KEY AUTOINCREMENT
- user_id: INTEGER (foreign key to users)
- item_type: TEXT
- quantity: INTEGER
- location: TEXT
- collection_date: TEXT
- status: TEXT (default: 'Pending')

## API Endpoints

- GET `/` - Home page
- GET/POST `/add_item` - Add new e-waste record
- GET `/view_data` - View all records
- GET `/statistics` - View statistics and reports
- GET `/about` - About page

## File Structure

```
e-waste-collection-recycling/
├── backend/
│   ├── app.py          # Main Flask application
│   ├── database.py     # Database connection and table creation
│   ├── models.py       # CRUD operations
│   ├── routes.py       # API routes
│   ├── report.py       # Report generation
│   ├── templates/      # HTML templates
│   └── static/         # CSS, JS, and other static files
├── database/
│   └── e_waste.db      # SQLite database file
├── requirements.txt    # Python dependencies
└── README.md
```

## Usage

1. Navigate to `/add_item` to add new e-waste records
2. View all records at `/view_data`
3. Get statistics and reports at `/statistics`
4. Use the edit/delete buttons on the view_data page to modify records

## Development

This project was developed as part of a 7-day plan:
- Day 1: Setup & Database Design
- Day 2: Backend Logic (CRUD Functions)
- Day 3: Frontend Skeleton
- Day 4: Connect Frontend with Backend
- Day 5: Update, Delete & Validation
- Day 6: Reports & Finishing Touches
- Day 7: Testing & Documentation