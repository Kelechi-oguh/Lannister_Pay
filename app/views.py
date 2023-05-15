from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Transaction, SplitInfo, TransactionResponse, SplitBreakdown
from .serializer import TransactionSerializer, SplitInfoSerializer, TransactionResponseSerializer

# Create your views here.


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "Description": {"message": "lANNISTER_PAY  A Flutterwave assigned task to create a transaction payment splitting service (TPSS)."},

            "Urls": {
                "home": reverse('home_view', request=request),
                "transaction_page": reverse('transaction_view', request=request)}
            }

        return Response(data)
    


class TransactionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cal = calculations(serializer.data['ID'])
            return Response(cal.data)
        return Response(serializer.errors)
    
    def get(self, request, *args, **kwargs):
        obj = TransactionResponse.objects.all()
        serializer = TransactionResponseSerializer(obj, many=True)
        return Response(serializer.data)

    




def calculations(transaction_id):
    transaction = Transaction.objects.get(ID=transaction_id)
    split = SplitInfo.objects.filter(transaction=transaction_id)  # a queryset of the splitinfo related to the given transactioin id

    balance = transaction.Amount

    tr_response = TransactionResponse(ID=transaction_id, Balance=balance)
    tr_response.save()

    flat_first = []
    percentage_second = []
    ratio_last = []

    for i in split:
        if i.SplitType == "FLAT":
            flat_first.append((i.SplitEntityId, i.SplitValue))

        elif i.SplitType == "PERCENTAGE":
            percentage_second.append((i.SplitEntityId, i.SplitValue))
        
        elif i.SplitType == "RATIO":
            ratio_last.append((i.SplitEntityId, i.SplitValue))

    
    for split_id, value in flat_first:
        if balance != 0:
            balance = balance - value
            split_breakdown = SplitBreakdown(transaction=tr_response, SplitEntityId=split_id, Amount=value)
            split_breakdown.save()

    for split_id, value in percentage_second:
        if balance != 0:
            amount = (value/100) * balance
            balance = balance - amount
            split_breakdown = SplitBreakdown(transaction=tr_response, SplitEntityId=split_id, Amount=amount)
            split_breakdown.save()

    total_ratio = 0
    for split_id, value in ratio_last:
        total_ratio = total_ratio + value   # Calculate the total ratio
    
    ratio_balance = balance

    for split_id, value in ratio_last:
        if ratio_balance != 0:
            amount = ratio_balance * (value/total_ratio)
            balance = balance - amount
            split_breakdown = SplitBreakdown(transaction=tr_response, SplitEntityId=split_id, Amount=amount)
            split_breakdown.save()

    tr_update = TransactionResponse.objects.get(ID=transaction_id)
    tr_update.Balance = balance
    tr_update.save()
    
    serializer = TransactionResponseSerializer(tr_update)
    return serializer
    


# learn how to document this api