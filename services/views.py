from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.decorators import action
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class ServiceListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        services = Service.objects.all()
        
        query = request.query_params.get('search', None)
        category = request.query_params.get('category', None)
        
        if query:
            services = services.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        if category:
            services = services.filter(category__name__iexact=category)
        
        
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class ServiceDetailAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return None
        
    def get(self, request, pk):
        service = self.get_object(pk)
        if service:
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        return Response({'error': 'Service not found!'})
    
    def put(self, request, pk):
        service = self.get_object(pk)
        if service:
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({'error': 'Service not found!'})
    
    def delete(self, request, pk):
        service = self.get_object(pk)
        if service:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Service not found!'})
            

class TopRatedServiceAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        top_rated = Service.objects.filter(rating__gt=0).order_by('-rating')[:10]
        serializer = ServiceSerializer(top_rated, many=True)
        return Response(serializer.data)




class ServiceReviewAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            service = Service.objects.get(id=pk)
        except Service.DoesNotExist:
            return Response({'error': "Service Not Found!"}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(service=service)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, pk):
        try:
            service = Service.objects.get(id=pk)
        except Service.DoesNotExist:
            return Response({'error': "Service Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        
        # data = request.data.copy()
        # data['user'] = request.user.id
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service=service, user=request.user)
            return Response(data=serializer.data)
        return Response(serializer.errors)
    
    
class ServiceReviewDetailAPIView(APIView):
    def get_object(self, review_id):
        try:
            return Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return None
        
    def get(self, request, pk, review_id):
        review = self.get_object(review_id)
        
        if review:
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        return Response({'error': 'Review not found!'})
    
    def put(self, request, pk, review_id):
        review = self.get_object(review_id)
        
        if review:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({'error': 'Review not found!'})
    
    
    def delete(self, request, pk, review_id):
        review = self.get_object(review_id)
        
        if review:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)     
        return Response({'error': 'Review not found!'})
    
   
    
        
    
        