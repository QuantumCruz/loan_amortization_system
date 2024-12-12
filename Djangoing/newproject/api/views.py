from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import profile, Transactions
from .serializer import ProfileSerializer, TransactionsSerializer

@api_view(['GET'])
def get_users(request):
    profiles = profile.objects.all()
    serializedData = ProfileSerializer(profiles, many=True).data
    return Response(serializedData)

@api_view(['POST'])
def create_profile(request):
    data = request.data
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        prof = profile.objects.get(pk=pk)
    except profile.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        prof.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        serializer = ProfileSerializer(prof, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def auth_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        prof = profile.objects.get(username=username, password=password)
        transactions = prof.transactions.all()
        serializer = TransactionsSerializer(transactions, many=True)
        return Response({"message": "User exists", "User_ID": prof.id, "Name": prof.name,
                        "Username": prof.username,
                        "Password": prof.password,
                        "Role": prof.role,
                        "Balance": prof.loan_amount,
                        "Role": prof.role,
                        "Phone": prof.phone,
                        "Address": prof.address,
                        "Transactions": serializer.data
                        }, status=status.HTTP_200_OK)
    except profile.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_transaction(request, pk):
    try:
        prof = profile.objects.get(pk=pk)
    except profile.DoesNotExist:
        return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    data['profile'] = pk
    serializer = TransactionsSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_profile_transactions(request, pk):
    try:
        prof = profile.objects.get(pk=pk)
    except profile.DoesNotExist:
        return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    transactions = prof.transactions.all()
    serializer = TransactionsSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_transactions(request):
    transactions = Transactions.objects.all()
    serializer = TransactionsSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)