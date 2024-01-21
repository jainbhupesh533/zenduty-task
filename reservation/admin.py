from django.contrib import admin

from .models.library_models import *

# Register your models here.
admin.register(Books)
admin.register(Members)
admin.register(ReservationQueue)
admin.register(Author)