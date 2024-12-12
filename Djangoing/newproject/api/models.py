from django.db import models
from dateutil.relativedelta import relativedelta
import datetime
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class profile(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    address = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=12, default='0000000000')
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    loan_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    loan_term = models.IntegerField(default=12)
    
    def __str__(self):
        return self.name


class Transactions(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    next_payment = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)
    state = models.CharField(max_length=50, default="Credit")
    profile = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='transactions')
    interest_on_loan = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.date.today()

        if self.state == "Credit": #Credit
            self.profile.loan_amount += self.amount
            self.next_payment = self.date + relativedelta(months=1)
                
            self.profile.save()
        else: #Debit
            self.profile.loan_amount -= self.amount
            self.next_payment = self.date + relativedelta(months=1)
            self.interest_on_loan = (self.amount * Decimal(25)) / Decimal(1000)
            self.profile.loan_amount -= self.interest_on_loan
            
            if self.profile.loan_amount >= 0:
                self.profile.loan_term = 12
                
            self.profile.save()
                

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.id} - {self.amount}"

@receiver(post_save, sender=profile)
def create_initial_transaction(sender, instance, created, **kwargs):
    if created:  # Only create a transaction for new profiles
        initial_transaction = Transactions(
            profile=instance, 
            amount=Decimal(0),
            state="Credit",  # Default state is Credit
            interest_on_loan=Decimal(0)
        )
        initial_transaction.save()
