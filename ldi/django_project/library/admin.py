from django.contrib import admin
from .models import Library, Category

# Register your models here.
try:
    admin.site.unregister(Library)
except admin.sites.NotRegistered:
    pass

# Define the custom StudentAdmin class
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']  # Adjust the fields as needed

# Register the Student model with the custom StudentAdmin class
admin.site.register(Library, StudentAdmin)
admin.site.register(Category)



