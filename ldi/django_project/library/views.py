from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Library, Category
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

# Create your views here.
def index(request):
    new_vision = Library.objects.filter(publication='New Vision')
    daily_monitor = Library.objects.filter(publication='Daily Monitor')

    return render(request, 'index.html', {
        'new_vision': new_vision,
        'daily_monitor': daily_monitor,
    })
# def home(request):
#     return render(request, 'home.html', {'library': Library.objects.all()})


def home(request):
    student = Library.objects.all()
    return render(request, 'home.html', {'library': Library.objects.all()})


def view_student(request):
    student = Library.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def library(request):
    query = request.GET.get('q')  # Search query
    publication_filter = request.GET.get('publication')  # Publication filter

    # Start with all records
    library = Library.objects.all()

    # Apply the search filter if there's a query
    if query:
        library = library.filter(
            title__icontains=query) | library.filter(
            author__icontains=query) | library.filter(
            date__icontains=query) | library.filter(
            location__icontains=query)
    
    # Apply the publication filter if one is selected
    if publication_filter:
        library = library.filter(publication__iexact=publication_filter)

    # Debugging output
    print(f"Query: {query}")
    print(f"Publication Filter: {publication_filter}")
    print(f"Filtered Records: {library}")

    context = {
        'library': library,
        'query': query,
        'publication_filter': publication_filter,  # Include publication filter in context
    }
    return render(request, 'home.html', context)




def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student = form.save(commit=False)
            # Assign any additional fields if needed
            new_student.save()
            return render(request, 'add.html', {
                'form': StudentForm(),
                'success': True
            })
    else:
        form = StudentForm()
    return render(request, 'add.html', {'form': form})


def edit(request, id):
    if request.method == 'POST':
        student = Library.objects.get(pk=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'edit.html', {
                'form': form,
                'success': True
            })
    else:
        student = Library.objects.get(pk=id)
        form = StudentForm(instance=student)
    return render(request, 'edit.html', {
        'form': form
    })             
            
def delete(request, id):
    if request.method == 'POST':
        student = Library.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))    


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('index')  # Ensure 'index' is the correct URL name
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..... Thanks for spending some time with us"))
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been registered successfully! Welcome!")
                return redirect('login')  # Make sure 'login' is the correct URL name
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('register')
        else:
            messages.error(request, "There was a problem with your registration. Please check the form and try again.")
            # Optionally, render the form with errors back to the user
            return render(request, 'register.html', {'form': form})
    else:    
        return render(request, 'register.html', {'form': form})

def category(request, foo):
    # replace hyphens with spaces
    foo = foo.replace('-', '')
    # grab the category from the url
    
    try:
        #look up the category
        category = Category.objects.get(name=foo)
        
        return render(request, 'category.html', {'category':category})
    except:
        messages.success(request, ("That Category Doesnot Exist........."))
        return redirect('index')                    
    
    