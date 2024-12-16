from rest_framework import viewsets, status
from .models import Author
from .serializers import AuthorSerializer
from .models import Book,BorrowRecord
from .serializers import BookSerializer,BorrowRecordSerializer, ReturnBookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.views import APIView
from .tasks import generate_report
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .tasks import generate_report
import json
import os
from django.conf import settings

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        """Custom create method to handle borrowing a book."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], url_path='return')
    def return_book(self, request, pk=None):
        """Mark a book as returned."""
        try:
            borrow_record = BorrowRecord.objects.get(pk=pk, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "Invalid borrow record or book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReturnBookSerializer(borrow_record, data={'return_date': now().date()}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Increase the available copies of the book
        book = borrow_record.book
        book.available_copies += 1
        book.save()

        return Response({"message": f"Book '{book.title}' has been returned."}, status=status.HTTP_200_OK)




class GenerateReportView(APIView):
    def post(self, request, *args, **kwargs):
        # Trigger the Celery task asynchronously
        generate_report.delay()  # Start generating the report in the background
        return Response({"message": "Report generation started."})

class LatestReportView(APIView):
    def get(self, request, *args, **kwargs):
        reports_dir = os.path.join(settings.BASE_DIR, 'reports')  # Adjust path as needed

        # Ensure the reports directory exists
        if not os.path.exists(reports_dir):
            return JsonResponse({'message': 'Reports directory does not exist.'}, status=404)

        try:
            reports = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
            if reports:
                latest_report = reports[-1]  # Assuming the latest report is the last one in the list
                return JsonResponse({'latest_report': latest_report})
            else:
                return JsonResponse({'message': 'No reports found.'}, status=404)
        except FileNotFoundError:
            return JsonResponse({'message': 'Reports directory does not exist.'}, status=404)

