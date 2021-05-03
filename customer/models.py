from django.db import models

# Create your models here.
class Customer(models.Model):
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    telephone_contact = models.CharField(max_length=100)
    DEPARTMENT_CHOICES = (
        ("Testing", "Testing"),
        ("Certification", "Certification"),
        ("Imports Inspection", "Imports Inspection"),
        ("UNBS Market Surveillance", "UNBS Market Surveillance"),
        ("Finance & Administration", "Finance & Administration"),
        ("Human Resource", "Human Resource"),
        ("Office of the Executive Director", "Office of the Executive Director")
    )

    department_to_vist = models.CharField(max_length=100, choices = DEPARTMENT_CHOICES)
    email = models.EmailField()
    visit_date = models.DateTimeField(auto_now_add=True)
    first_time_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
    

class Feedback(models.Model):
    were_you_served = models.BooleanField(default=False)
    reason_or_feedback = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.company_name
    