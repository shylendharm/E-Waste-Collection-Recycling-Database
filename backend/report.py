from backend.models import get_ewaste_statistics

def generate_report():
    """Generate a summary report of e-waste collection"""
    stats = get_ewaste_statistics()
    
    report = {
        "total_records": stats["total_records"],
        "status_breakdown": stats["status_counts"],
        "item_type_breakdown": stats["type_counts"],
        "summary": f"Total e-waste records: {stats['total_records']}. "
                   f"Collected items: {stats['status_counts'].get('Collected', 0)}. "
                   f"Pending items: {stats['status_counts'].get('Pending', 0)}. "
    }
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print("E-Waste Collection Report:")
    print(f"Total Records: {report['total_records']}")
    print(f"Status Breakdown: {report['status_breakdown']}")
    print(f"Item Type Breakdown: {report['item_type_breakdown']}")
    print(f"Summary: {report['summary']}")