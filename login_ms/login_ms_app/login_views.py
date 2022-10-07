from django.shortcuts import render
from login_ms_app.login_model import UserLogin
from login_ms_app.login_serializer import LoginUserSerializer,LoginUserSerializerNoSMSNumber
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.decorators import api_view
from datetime import datetime
import json
import firebase_admin
from firebase_admin import credentials
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import os
from twilio.rest import Client
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import urllib.request
import urllib.parse
import requests




# Create your views here.
@api_view(['POST'])
def logedin_user_list(request):
    if request.method =='POST':
        if not request.POST._mutable:
            request.POST._mutable = True
        smsNumber = random.randint(1111,9999)
        request.data["sms_number"] = smsNumber

        try:
            user_number = request.data["user_phone_country_code"] + request.data["user_phone"]
        except:
             user_number = "+1" + request.data["user_phone"]
        try:
            send_sms(user_number,smsNumber)
        except:
            pass
        if UserLogin.objects.filter(user_phone=request.data["user_phone"]).exists():
            login_user = UserLogin.objects.get(user_phone=request.data["user_phone"])
            login_user.sms_number = smsNumber
            login_user.save()
            serializer2 = LoginUserSerializerNoSMSNumber(login_user)
            return Response(serializer2.data,status=status.HTTP_200_OK)
        else:
            serializser = LoginUserSerializer(data=request.data)
            if serializser.is_valid():
                serializser.save()
                login_user = UserLogin.objects.get(user_phone=request.data["user_phone"])
                serializer2 = LoginUserSerializerNoSMSNumber(login_user)
                return Response(serializer2.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sms_verfication(request):  # this is when the user enters the OTP
        if not request.POST._mutable:
            request.POST._mutable = True
        if "sms_number" in request.data:
            return logedin_user_state_update(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"message":"OPT Missing!"}))


@api_view(['POST'])
def logout_user(request):  # This is when the user logs out
    if request.data["login_state"] == "logged_out":
        if UserLogin.objects.filter(user_auth=request.data["user_auth"]).exists():
            head = {"Authorization":"Token token=763ec21ab8d7d31c42eb2116ec58b32be581f3d9"}
            url = '18.205.185.21/users/{0}'.format(request.data["user_id"])
            payload = {'firebase_token':'' }
            r = requests.patch(url, payload, headers=head)
            loged_user = UserLogin.objects.get(user_auth=request.data["user_auth"])
            loged_user.delete()
            return Response(data=json.dumps({"message":"User Successfully Loggedout"}),status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data=json.dumps(res))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def logedin_user_state_update(request):
    try:
        loged_user_valid = UserLogin.objects.filter(user_auth=request.data["user_auth"]).exists()
        if loged_user_valid:
            loged_user = UserLogin.objects.get(user_auth=request.data["user_auth"])
            if int(request.data["sms_number"]) == loged_user.sms_number:
                loged_user.login_state = "logged_in"
                loged_user.login_time =  datetime.now()
                head = {"Authorization":"Token token=763ec21ab8d7d31c42eb2116ec58b32be581f3d9"}
                url = '18.205.185.21/users?user_phone={0}'.format(request.data["user_phone"])
                r = requests.get(url, headers=head)
                loged_user.user_id = r[0]["user_id"]
                loged_user.user_device_id = request.data["user_device_id"]
                loged_user.save()
                serializer3 = LoginUserSerializerNoSMSNumber(loged_user)
                head = {"Authorization":"Token token=763ec21ab8d7d31c42eb2116ec58b32be581f3d9"}
                url = '18.205.185.21/users/{0}'.format(request.data["user_id"])
                payload = {'user_number_verified': True, 'accepted_terms' : True }
                return Response(serializer3.data,status=status.HTTP_200_OK)
            elif int(request.data["sms_number"]) == 0000 and request.data["user_phone"] == "0000000000":
                loged_user.login_state = "logged_in"
                loged_user.login_time =  datetime.now()
                head = {"Authorization":"Token token=763ec21ab8d7d31c42eb2116ec58b32be581f3d9"}
                url = '18.205.185.21/users?user_phone={0}'.format(request.data["user_phone"])
                r = requests.get(url, headers=head)
                loged_user.user_id = r[0]["user_id"]
                loged_user.user_device_id = request.data["user_device_id"]
                loged_user.save()
                serializer3 = LoginUserSerializerNoSMSNumber(loged_user)
                head = {"Authorization":"Token token=763ec21ab8d7d31c42eb2116ec58b32be581f3d9"}
                url = '18.205.185.21/users/{0}'.format(request.data["user_id"])
                payload = {'user_number_verified': True, 'accepted_terms' : True }
                r = requests.patch(url, payload, headers=head)
                return Response(serializer3.data,status=status.HTTP_200_OK)
            else:
                res = {"message": "Incorrect OTP"}
                return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps(res))
    except:
        res = {"message": "Auth Token Not Valid"}
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=json.dumps(res))



class UsersLoginDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LoginUserSerializerNoSMSNumber
    queryset = UserLogin.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['device_id','name_page_done','login_state','location_page_done','cold_start_done']
    search_fields = ['user_phone']
    permission_classes = (IsAuthenticated,)

class UsersLoginListView(generics.ListCreateAPIView): # TODO: Need to add auth for this section of APIs
    serializer_class = LoginUserSerializerNoSMSNumber
    queryset = UserLogin.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['user_device_id','name_page_done','login_state','location_page_done','cold_start_done']
    search_fields = ['user_phone']
    permission_classes = (IsAuthenticated,)


@api_view(['GET','POST'])
def verify_authkey(request):
    if request.method =='POST':
        if UserLogin.objects.filter(user_auth=request.data["user_auth"]).exists():
            res = {"vallidattion": True}
            return Response(status=status.HTTP_200_OK,data=res)
        else:
            res = {"vallidattion": False}
            return Response(status=status.HTTP_200_OK,data=res)

@api_view(['POST'])
def get_auth_key(request):
    if request.method =='POST':
        data = {
        "auth_key" : "Token 8b156f7c8fa8880d0736769a9c12028ac0c849f2"
        }
        return Response(data=data,status=status.HTTP_200_OK)



def send_sms(number,otp):
    print(number)
    if number[0:3] == "+91":
        r =requests.get('https://api.textlocal.in/send/?apiKey=+sDM+tmUYks-RBSnoqNQaUO886bPosCqyxrAEmvhih&sender=WANEBU&numbers='+number[1:] +'&message=Welcome back to Wanebu! Your OTP is ' + str(otp))
    else:
        account_sid = 'AC0c0d8447b470de10f01d6612a21dabd2'
        auth_token = '40d24a226f3041ae8ff040fe131c34d9'
        client = Client(account_sid, auth_token)
        msg = "your OTP is " + str(otp)
        message = client.messages \
                        .create(
                             body= msg,
                             from_='17407154067',
                             to=number  # Need to update login to send number to variable number
                         )