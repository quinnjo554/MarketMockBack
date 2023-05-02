from django.contrib import admin

# Register your models here.
# FOR EVERY NEW MODEL YOU MUST REGISTER TO USE IN ADMIN
from.models import User, Stock, UserStock

admin.site.register(User)
admin.site.register(Stock)
admin.site.register(UserStock)

