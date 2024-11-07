# books/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Book, Review, Cart
from .serializers import BookSerializer, ReviewSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated
import os

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        book = self.get_object()
        cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
        if created:
            return Response({'status': 'book added to cart'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'book already in cart'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout(self, request):
        # Mock payment logic (replace with actual payment integration)
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            item.delete()  # Clear the cart after payment

        return Response({'status': 'Payment successful'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def download(self, request, pk=None):
        # Check if payment has been made (simplified logic here)
        book = self.get_object()
        if Cart.objects.filter(user=request.user, book=book).exists():
            filepath = book.pdf_file.path
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    response = HttpResponse(f.read(), content_type="application/pdf")
                    response['Content-Disposition'] = f'inline; filename={os.path.basename(filepath)}'
                    return response
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Payment required'}, status=status.HTTP_402_PAYMENT_REQUIRED)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
