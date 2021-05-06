from django.shortcuts import render, redirect
from .models import Customer, Feedback
from .forms import CustomerForm, FeedbackForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
# from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_feedback_email(customer, request):
    current_site = get_current_site(request)
    email_subject = 'Submit your Feedback'
    email_body = render_to_string('customer/email_feedback.html', {
        'customer' : customer,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(customer.pk)),
        # 'token' : generate_token.make_token(customer)
    })

    email = EmailMessage(subject=email_subject, body = email_body, from_email = settings.EMAIL_FROM_USER, to = [customer.email,])
    EmailThread(email).start()
    # email.send()

# Create your views here.
@login_required
def home(request):
    companies = Customer.objects.all()
    return render(request, 'customer/index.html', { 'companies':companies })

@login_required
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
            customer = form.save()
            print(customer)

            # send email to provide feedback
            send_feedback_email(customer, request)
            messages.add_message(request, messages.SUCCESS, "Company Added Please Check your email to give feedback about your experience at the UNBS frontdesk")
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

@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.add_message(request, messages.SUCCESS, f"You have successfully logged out")
        return redirect('login')

def get_customer_feedback(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        customer = Customer.objects.get(pk=uid)
    except Exception as e:
        customer = None

    # if customer and generate_token.check_token(customer, token):
    if customer:
        return redirect('add_feedback', customer.id)

def add_feedback(request, id):
    customer = Customer.objects.get(pk=id)
    form = FeedbackForm()
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback()
            feedback.provided_feedback = True
            feedback.were_you_served = form.cleaned_data.get('were_you_served')
            feedback.reason_or_feedback = form.cleaned_data.get('reason_or_feedback')
            feedback.customer = customer
            feedback.save()
            messages.add_message(request, messages.SUCCESS, f"Thankyou for your feedback")
            return redirect('home')
    return render(request, 'customer/add_feedback.html', {'customer':customer, 'form':form})

