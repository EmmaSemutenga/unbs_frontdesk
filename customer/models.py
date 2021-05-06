from django.db import models

# Create your models here.
class Customer(models.Model):
    company_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    contact_person = models.CharField(max_length=100, null=True)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(max_length=20, choices = GENDER_CHOICES, null=True)
    telephone_contact = models.CharField(max_length=100, null=True)
    DEPARTMENT_CHOICES = (
        ("Testing", "Testing"),
        ("Certification", "Certification"),
        ("Imports Inspection", "Imports Inspection"),
        ("UNBS Market Surveillance", "UNBS Market Surveillance"),
        ("Finance & Administration", "Finance & Administration"),
        ("Human Resource", "Human Resource"),
        ("Office of the Executive Director", "Office of the Executive Director")
    )

    department_to_vist = models.CharField(max_length=100, choices = DEPARTMENT_CHOICES, null=True)
    email = models.EmailField(null=True)
    visit_date = models.DateTimeField(auto_now_add=True, null=True)
    first_time_customer = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.company_name
    

class Feedback(models.Model):
    provided_feedback = models.BooleanField(default=False)
    were_you_served = models.BooleanField(default=False)
    reason_or_feedback = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.company_name
    