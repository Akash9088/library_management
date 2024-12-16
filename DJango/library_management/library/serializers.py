from rest_framework import serializers
from .models import Author
from .models import BorrowRecord, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'available_copies']

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrowed_by', 'borrow_date', 'return_date']

    def validate(self, data):
        """Custom validation to ensure the book has available copies."""
        book = data['book']
        if book.available_copies < 1:
            raise serializers.ValidationError(f"The book '{book.title}' is currently not available for borrowing.")
        return data

    def create(self, validated_data):
        """Custom create method to reduce the available copies of the book."""
        book = validated_data['book']
        book.available_copies -= 1
        book.save()
        return super().create(validated_data)

class ReturnBookSerializer(serializers.ModelSerializer):
    """Serializer for marking a book as returned."""
    class Meta:
        model = BorrowRecord
        fields = ['return_date']