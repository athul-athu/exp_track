from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Item, UserDetails, TransactionDetails
from .serializers import ItemSerializer, UserDetailsSerializer, TransactionDetailsSerializer
import uuid
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'items': reverse('item-list', request=request, format=format),
        'users': reverse('userdetails-list', request=request, format=format),
        'create_user': reverse('create-user', request=request, format=format),
        'get_all_users': reverse('get-all-users', request=request, format=format),
        'create_transaction': reverse('create-transaction', request=request, format=format),
    })

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # If profile_img is provided in request, update the user
        profile_img = request.data.get('profile_img')
        if profile_img:
            user.profile_img = profile_img
            user.save()
        return Response({
            'status': 'success',
            'message': 'User created successfully',
            'data': {
                'user_id': user.user_id,
                'token': user.token,
                'name': user.name,
                'phone_number': user.phone_number,
                'profile_img': user.profile_img if user.profile_img else None
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'message': 'Invalid data provided',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    # Validate input
    if not phone_number or not password:
        return Response({
            'status': 'error',
            'message': 'Phone number and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find user by phone number
        user = UserDetails.objects.get(phone_number=phone_number)
        
        # Check password
        if user.check_password(password):
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'user_id': user.user_id,
                    'token': user.token,
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'age': user.age,
                    'bank_account_name': user.bank_account_name,
                    'profile_img': user.profile_img
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid password'
            }, status=status.HTTP_401_UNAUTHORIZED)

    except ObjectDoesNotExist:
        return Response({
            'status': 'error',
            'message': 'User not found with this phone number'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    try:
        users = UserDetails.objects.all().order_by('name')  # Get all users ordered by name
        serializer = UserDetailsSerializer(users, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Users retrieved successfully',
            'total_users': len(serializer.data),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_transaction(request):
    """
    Create a new transaction detail entry with token-based authorization.
    Token should be passed in the Authorization header as 'Bearer <token>'
    """
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({
            'status': 'error',
            'message': 'Authorization header with Bearer token is required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    
    try:
        # Find user by token
        user = UserDetails.objects.get(token=token)
    except ObjectDoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Invalid token or user not found'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Validate required fields
    amount = request.data.get('amount')
    transaction_type = request.data.get('transaction_type')
    date_str = request.data.get('date')
    
    if not amount or not transaction_type:
        return Response({
            'status': 'error',
            'message': 'amount and transaction_type are required fields'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate transaction type
    valid_types = ['INCOME', 'EXPENSE', 'TRANSFER', 'REFUND']
    if transaction_type not in valid_types:
        return Response({
            'status': 'error',
            'message': f'transaction_type must be one of: {", ".join(valid_types)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Parse date if provided, otherwise use current date
    try:
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        else:
            date = datetime.now()
    except ValueError:
        return Response({
            'status': 'error',
            'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create transaction data
    transaction_data = {
        'user': user.user_id,
        'amount': amount,
        'transaction_type': transaction_type,
        'date': date,
        'description': request.data.get('description'),
        'category': request.data.get('category'),
        'is_recurring': request.data.get('is_recurring', False),
        'recurring_frequency': request.data.get('recurring_frequency')
    }
    
    # Create serializer and validate
    serializer = TransactionDetailsSerializer(data=transaction_data)
    if serializer.is_valid():
        transaction = serializer.save()
        return Response({
            'status': 'success',
            'message': 'Transaction created successfully',
            'data': {
                'id': transaction.id,
                'user_id': transaction.user.user_id,
                'amount': str(transaction.amount),
                'transaction_type': transaction.transaction_type,
                'description': transaction.description,
                'category': transaction.category,
                'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S'),
                'is_recurring': transaction.is_recurring,
                'recurring_frequency': transaction.recurring_frequency
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'status': 'error',
            'message': 'Invalid transaction data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
