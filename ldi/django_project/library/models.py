from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Library(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    date = models.DateField(default='2023-01-01')
    location = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Adding Category as a foreign key
    publication = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return f'{self.title}'

