# from rest_framework import serializers
# from .models import profile,Transactions
# from dateutil.relativedelta import relativedelta
        
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = profile
#         fields = "__all__"
# class TransactionsSerializer(serializers.ModelSerializer):
#     profile_name = serializers.CharField(source='profile.name', read_only=True)
#     class Meta:
#         model = Transactions
#         fields = ['id', 'date', 'amount', 'state', 'profile_name', 'next_payment', 'interest_on_loan']
        
#     def create(self, validated_data):
#         validated_data['next_payment'] = validated_data.get('next_payment', None)
#         return super().create(validated_data)

from rest_framework import serializers
from .models import profile, Transactions

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = "__all__"

class TransactionsSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    
    # Make sure to accept a profile ID for creation (or a nested profile serializer)
    profile_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Transactions
        fields = ['id', 'date', 'amount', 'state', 'profile_name', 'next_payment', 'interest_on_loan', 'profile_id']
        
    def create(self, validated_data):
        profile_id = validated_data.pop('profile_id')
        
        # Get the profile instance using the ID
        try:
            profile_instance = profile.objects.get(id=profile_id)
        except profile.DoesNotExist:
            raise serializers.ValidationError(f"Profile with ID {profile_id} does not exist.")

        # Create the transaction and link it to the profile
        transaction = Transactions.objects.create(profile=profile_instance, **validated_data)
        
        return transaction
