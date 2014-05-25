from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "currencies"

    def __unicode__(self):
        return self.symbol + " -- " + self.name


class account_category:
    # negative = payment
    funding_source = "fund"

    # positive = expense
    expenses = "exp"

    other = "other"

ACCOUNT_CATEGORY_CHOICES = (
    (account_category.funding_source, "Funding source"),
    (account_category.expenses, "Expenses"),
    (account_category.other, "Other"),
    )


class AccountGroup(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    group = models.ForeignKey(AccountGroup)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    currency = models.ForeignKey(Currency)

    category = models.CharField(max_length=10,
            choices=ACCOUNT_CATEGORY_CHOICES)

    guardian = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.symbol + " -- " + self.name

    class Meta:
        ordering = ["symbol"]

    def balance(self):
        from decimal import Decimal

        TWO_PLACES = Decimal(10) ** -2

        result = Decimal(0)
        for ec in self.entry_components.all():
            result += ec.amount

        return result.quantize(TWO_PLACES)


class EntryCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "entry categories"

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    valid_date = models.DateField(default=now)

    description = models.CharField(max_length=200)

    create_date = models.DateTimeField(default=now)
    creator = models.ForeignKey(User)

    category = models.ForeignKey(EntryCategory)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["valid_date", "description"]

    def __unicode__(self):
        return "%s (%s)" % (
                self.description,
                self.valid_date)


class EntryComponent(models.Model):
    entry = models.ForeignKey(Entry, related_name="components")
    account = models.ForeignKey(Account,
            related_name="entry_components")
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        ordering = ["amount"]


class EntryComment(models.Model):
    entry = models.ForeignKey(Entry)
    create_date = models.DateTimeField(default=now)
    creator = models.ForeignKey(User)

    comment = models.TextField()


class EntryValidation(models.Model):
    entry_component = models.ForeignKey(EntryComponent)
    create_date = models.DateTimeField(default=now)
    validator = models.ForeignKey(User)

    comments = models.TextField(null=True, blank=True)
