from rest_framework import serializers
from login_ms_app.login_model import UserLogin

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'
        depth = 1


class LoginUserSerializerNoSMSNumber(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['user_id','user_auth','login_time','logout_time','user_phone','user_phone_country_code','login_state','user_device_id','name_page_done','location_page_done','cold_start_done','firebase_token']
        depth = 1