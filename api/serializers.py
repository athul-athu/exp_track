from rest_framework import serializers
from .models import Item, UserDetails, TransactionDetails

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class UserDetailsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserDetails
        fields = ['user_id', 'name', 'phone_number', 'profile_img', 'age', 'bank_account_name', 'token', 'password']
        read_only_fields = ['user_id', 'token']  # These fields are auto-generated 
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_img': {'required': False, 'allow_null': True}
        }

class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = ['id', 'user', 'amount', 'transaction_type', 'description', 'category', 'date', 'is_recurring', 'recurring_frequency']
        read_only_fields = ['id', 'date']  # These fields are auto-generated
        extra_kwargs = {
            'description': {'required': False, 'allow_null': True},
            'category': {'required': False, 'allow_null': True},
            'is_recurring': {'required': False, 'default': False},
            'recurring_frequency': {'required': False, 'allow_null': True}
        } 