from django.db import models as m
import uuid


# Create your models here.
class Service(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=40, unique=True)
    fee = m.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.fee}"


class Transaction(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = m.DateTimeField(auto_now_add=True)
    user = m.ForeignKey('accounts.User', on_delete=m.CASCADE, related_name="transactions")
    amount = m.PositiveIntegerField()


class Test(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=40, unique=True)
    price = m.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}"


class Consultation(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=40, unique=True)
    price = m.PositiveIntegerField()


class Drug(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=40, unique=True)
    price = m.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}"


class DrugStat(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = m.ForeignKey('Drug', on_delete=m.CASCADE, related_name='drug_records')
    total = m.PositiveIntegerField()
    time_created = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug} - {self.total}"


class ServiceStat(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = m.ForeignKey('Service', on_delete=m.CASCADE, related_name='service_records')
    total = m.PositiveIntegerField()
    time_created = m.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service} - {self.total}"


class LabStat(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = m.ForeignKey('Test', on_delete=m.CASCADE, related_name='lab_records')
    total = m.PositiveIntegerField()
    time_created = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test} - {self.total}"


class Receipt(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = m.DateTimeField(auto_now_add=True)
    user = m.ForeignKey('accounts.User', on_delete=m.CASCADE, related_name='receipts')
    ward_cost = m.PositiveIntegerField()
    days_in_ward = m.PositiveSmallIntegerField()
    consultations = m.ManyToManyField('Consultation', related_name='receipts')
    services = m.ManyToManyField('ServiceStat', related_name='receipts')
    tests = m.ManyToManyField('LabStat', related_name='receipts')
    drugs = m.ManyToManyField('DrugStat', related_name='receipts')
    consumables = m.PositiveIntegerField()
    pharmacy_bag = m.BooleanField(default=True)
    total = m.PositiveIntegerField()
    paid = m.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} {self.date}"
