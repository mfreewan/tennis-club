import uuid
from django.db import models
from django.urls import reverse #used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #required to assingn user in borrower
# Create your models here.

## create a model for the genre will contain name field 
 
class Genre(models.Model):
    name=models.CharField(max_length=200,help_text="Enter a Book genre (e.g. Science Fiction)")

    def __str__(self):
        """String for rapresenting the mode object"""
        return self.name
   
    
## Create a model for language will contain name field

class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100, null=True) # Allow null values

    def __str__(self):
        """String for rapresenting the mode object"""
        return self.name
        

## create a model for the book will contain title , author , summary ,isbn , genre , language

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    summary=models.TextField(max_length=1000, help_text="Enter a breif discribtion for the book ")
    isbn=models.CharField("ISBN",max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content"')
    genre=models.ManyToManyField(Genre,help_text="Select a genre for this book ")
    language=models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        """string for representing the model object """
        return self.title

    def get_absolute_url(self):
        """returns the url to access a detail record for this book"""
        return reverse('book-detail',args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'
    
   
## create  a model for book instance will contain book , imprint , due back , id , status , borrower
class BookInstance(models.Model):                                                                       
    book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book acroos whole library ')
    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reversed'),
    )
    status=models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text='Book availability')
    borrower=models.ForeignKey( User ,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
         ordering=['due_back']

    def __str__(self):
        """string for representing the model object """
        return f'{self.id} ({self.book.title})'

##Create a model for author will conain name , Date of birth , Date of Death , books

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField(null=True,blank=True)

    class Meta:
        ordering=['last_name','first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance""" 
        return reverse('author-detail',args=[str(self.id)])
       
    def __str__(self):
         """string for representing the model object """
         return f'{self.last_name} ({self.first_name})'






















