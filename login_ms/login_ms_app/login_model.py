from django.db import models
import uuid
import datetime

class UserLogin(models.Model):
    loginState = (
    ('phone_verification_pending',"phone_verification_pending"),
    ("logged_in", "logged_in"),
    ("logged_out", "logged_out"),
    )

    user_id = models.UUIDField(null=True,blank=True)
    user_auth = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        primary_key=True,
    )
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True,blank=True)
    user_phone = models.CharField(max_length=20,null=True)
    user_phone_country_code = models.CharField(max_length=8,default="+1")
    sms_number = models.IntegerField(blank=True, null=True)
    login_state = models.CharField(max_length=100,choices=loginState,default="phone_verification_pending")
    device_id = models.BooleanField(default=False)
    user_device_id = models.CharField(max_length=400,null=True)
    name_page_done = models.BooleanField(default=False)
    location_page_done = models.BooleanField(default=False)
    cold_start_done = models.BooleanField(default=False)
    firebase_token = models.CharField(max_length=400,null=True)