from django.shortcuts import render, redirect
from .models import Customer, Feedback
from .forms import CustomerForm
from django.contrib import messages

# Create your views here.
def home(request):
    companies = Customer.objects.all()
    return render(request, 'customer/index.html', { 'companies':companies })

def add_company(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # customer = Customer()
            # customer.title = form.cleaned_data.get('title')
            
            # print("cleaned data here:", form.cleaned_data.get('title'))
            # todo = form.save()
            # print(todo.id)
            #customer.owner = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, "Company Added")
            return redirect('home')
    return render(request, 'customer/add_company.html', {'form':form, "value":"Add Customer"})

def login_user(request):
    if request.method == 'POST':
        context = {'data':request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, "invalid credentials")
            return render(request, "customer/login.html", {'data':context['data']})

        login(request, user)
        messages.add_message(request, messages.SUCCESS, f"Welcome {user.username} ")
        return redirect('home')
    return render(request, "customer/login.html")

def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.SUCCESS, f"You have successfully logged out")
        return redirect('login')