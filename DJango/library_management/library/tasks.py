# library/tasks.py
from celery import shared_task
from .models import Book, Author, BorrowRecord
import json
from datetime import datetime

@shared_task
def generate_report():
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    total_borrowed_books = BorrowRecord.objects.filter(return_date=None).count()

    report = {
        'total_authors': total_authors,
        'total_books': total_books,
        'total_borrowed_books': total_borrowed_books,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # Save the report to a file
    file_name = f"reports/report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(file_name, 'w') as report_file:
        json.dump(report, report_file)

    return report
