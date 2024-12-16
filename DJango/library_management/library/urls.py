# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, BorrowRecordViewSet, GenerateReportView, LatestReportView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrow', BorrowRecordViewSet, basename='borrow')

urlpatterns = [
    path('', include(router.urls)),
    path('reports/', GenerateReportView.as_view(), name='generate_report'),  # Endpoint to trigger report generation
    path('reports/latest/', LatestReportView.as_view(), name='latest_report'),  # Endpoint to get the latest report
]
