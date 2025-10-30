from backend.models import get_ewaste_statistics

def generate_report():
    """Generate a summary report of e-waste collection"""
    try:
        stats = get_ewaste_statistics()
        
        # Handle the case where stats might be None or empty
        if not stats:
            stats = {
                "total_records": 0,
                "status_counts": {},
                "type_counts": {}
            }
        
        # Ensure all expected fields exist in stats
        total_records = stats.get("total_records", 0) or 0
        status_counts = stats.get("status_counts", {}) or {}
        type_counts = stats.get("type_counts", {}) or {}
        
        # Ensure all expected status keys are present in the breakdown
        all_status_keys = ['Collected', 'Pending']  # Add other possible statuses as needed
        for key in all_status_keys:
            if key not in status_counts:
                status_counts[key] = 0
        
        collected_count = status_counts.get('Collected', 0) or 0
        pending_count = status_counts.get('Pending', 0) or 0
        
        report = {
            "total_records": total_records,
            "status_breakdown": status_counts,
            "item_type_breakdown": type_counts,
            "collected_count": collected_count,
            "pending_count": pending_count,
            "summary": f"Total e-waste records: {total_records}. "
                       f"Collected items: {collected_count}. "
                       f"Pending items: {pending_count}. "
        }
        
        return report
    except Exception as e:
        # In case of any error, return a default report
        report = {
            "total_records": 0,
            "status_breakdown": {"Collected": 0, "Pending": 0},
            "item_type_breakdown": {},
            "collected_count": 0,
            "pending_count": 0,
            "summary": "Error generating report. No statistics available."
        }
        print(f"Error generating report: {e}")
        return report

if __name__ == "__main__":
    report = generate_report()
    print("E-Waste Collection Report:")
    print(f"Total Records: {report['total_records']}")
    print(f"Status Breakdown: {report['status_breakdown']}")
    print(f"Item Type Breakdown: {report['item_type_breakdown']}")
    print(f"Summary: {report['summary']}")