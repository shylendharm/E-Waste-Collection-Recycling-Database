from flask import request, jsonify, render_template, redirect, url_for
from backend.models import (
    create_user, get_user_by_id, get_all_users, update_user, delete_user,
    add_ewaste_record, get_ewaste_record_by_id, get_all_ewaste_records, 
    update_ewaste_record, delete_ewaste_record, get_user_ewaste_records,
    get_ewaste_statistics
)

def register_routes(app):
    """Register all routes for the application"""
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/add_item', methods=['GET', 'POST'])
    def add_item():
        """Add a new e-waste record"""
        if request.method == 'POST':
            data = request.form
            try:
                result = add_ewaste_record(
                    user_id=int(data['user_id']),
                    item_type=data['item_type'],
                    quantity=int(data['quantity']),
                    location=data['location'],
                    collection_date=data['collection_date'],
                    status=data.get('status', 'Pending')
                )
                if result['success']:
                    # Redirect to view_data page after successful addition
                    return redirect(url_for('view_data'))
                else:
                    # In a real app, you'd show an error message
                    return jsonify(result), 400
            except ValueError:
                # Handle invalid input
                return jsonify({"success": False, "error": "Invalid input data"}), 400
        return render_template('add_item.html')
    
    @app.route('/view_data')
    def view_data():
        """View all e-waste records"""
        records = get_all_ewaste_records()
        return render_template('view_data.html', records=records)
    
    @app.route('/users', methods=['GET', 'POST'])
    def users():
        """Handle user operations"""
        if request.method == 'POST':
            data = request.form
            result = create_user(
                name=data['name'],
                email=data['email'],
                password=data['password']
            )
            return jsonify(result)
        else:
            users = get_all_users()
            return jsonify(users)
    
    @app.route('/ewaste_records', methods=['GET'])
    def ewaste_records():
        """Get all e-waste records"""
        records = get_all_ewaste_records()
        return jsonify(records)
    
    @app.route('/ewaste_records/<int:record_id>', methods=['GET', 'PUT', 'DELETE'])
    def ewaste_record(record_id):
        """Get, update, or delete a specific e-waste record"""
        if request.method == 'GET':
            record = get_ewaste_record_by_id(record_id)
            if record:
                return jsonify(record)
            else:
                return jsonify({"error": "Record not found"}), 404
        
        elif request.method == 'PUT':
            data = request.get_json()
            result = update_ewaste_record(
                record_id,
                user_id=data.get('user_id'),
                item_type=data.get('item_type'),
                quantity=data.get('quantity'),
                location=data.get('location'),
                collection_date=data.get('collection_date'),
                status=data.get('status')
            )
            return jsonify(result)
        
        elif request.method == 'DELETE':
            result = delete_ewaste_record(record_id)
            return jsonify(result)
    
    @app.route('/ewaste_records/user/<int:user_id>')
    def user_ewaste_records(user_id):
        """Get all e-waste records for a specific user"""
        records = get_user_ewaste_records(user_id)
        return jsonify(records)
    
    @app.route('/statistics')
    def statistics():
        """Get e-waste statistics"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from report import generate_report
        report = generate_report()
        return render_template('statistics.html', report=report)
    
    @app.route('/export_data')
    def export_data():
        """Export all e-waste records to a text file"""
        from flask import Response
        from backend.models import get_all_ewaste_records
        import json
        
        records = get_all_ewaste_records()
        
        # Format the data as a text report
        output = "E-Waste Collection Report\n"
        output += "=========================\n\n"
        output += f"Total Records: {len(records)}\n\n"
        output += "Detailed Records:\n"
        output += "-----------------\n"
        
        for record in records:
            output += f"ID: {record['record_id']}\n"
            output += f"User: {record['user_name'] or 'N/A'}\n"
            output += f"Item Type: {record['item_type']}\n"
            output += f"Quantity: {record['quantity']}\n"
            output += f"Location: {record['location']}\n"
            output += f"Collection Date: {record['collection_date']}\n"
            output += f"Status: {record['status']}\n"
            output += "-----------------\n"
        
        # Add statistics
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from report import generate_report
        stats = generate_report()
        
        output += "\nStatistics Summary:\n"
        output += "------------------\n"
        output += f"Total Records: {stats['total_records']}\n"
        output += f"Status Breakdown: {stats['status_breakdown']}\n"
        output += f"Item Type Breakdown: {stats['item_type_breakdown']}\n"
        output += f"Summary: {stats['summary']}\n"
        
        # Return as a downloadable text file
        return Response(
            output,
            mimetype="text/plain",
            headers={"Content-Disposition": "attachment; filename=ewaste_report.txt"}
        )
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html')
    
    # API endpoints for AJAX requests (for update/delete)
    @app.route('/api/update_record/<int:record_id>', methods=['POST'])
    def api_update_record(record_id):
        """Update a record via API call"""
        data = request.get_json()
        result = update_ewaste_record(
            record_id,
            item_type=data.get('item_type'),
            quantity=data.get('quantity'),
            location=data.get('location'),
            collection_date=data.get('collection_date'),
            status=data.get('status')
        )
        return jsonify(result)
    
    @app.route('/api/delete_record/<int:record_id>', methods=['POST'])
    def api_delete_record(record_id):
        """Delete a record via API call"""
        result = delete_ewaste_record(record_id)
        return jsonify(result)