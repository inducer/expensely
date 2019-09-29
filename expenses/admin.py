from django.contrib import admin
from expenses.models import (
        Currency,
        AccountGroup, Account,
        Entry, EntryComponent, EntryComment, EntryCategory)

from decimal import Decimal

TWO_PLACES = Decimal(10) ** -2


admin.site.register(Currency)
admin.site.register(AccountGroup)


class AccountAdmin(admin.ModelAdmin):
    list_filter = ('group', 'currency', 'category')
    list_display = ('id', 'symbol', 'name', 'group',
            'currency', 'category', 'guardian')
    list_editable = ('symbol', 'name', 'group', 'currency', 'category', 'guardian')


admin.site.register(Account, AccountAdmin)

admin.site.register(EntryCategory)


class EntryComponentInline(admin.TabularInline):
    model = EntryComponent
    extra = 2


class EntryCommentInline(admin.TabularInline):
    model = EntryComment
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = (
            'id',
            'description',
            'valid_date',
            'create_date',
            'creator',
            'category',
            'entry_amount')

    list_editable = (
            'description',
            'valid_date',
            'category')

    inlines = [
            EntryComponentInline,
            EntryCommentInline]

    def entry_amount(self, entry):
        amount = Decimal(0)
        for comp in entry.components.all():
            if comp.amount > 0:
                amount += Decimal(comp.amount)

        return amount.quantize(TWO_PLACES)

    date_hierarchy = "valid_date"

    list_filter = ('creator', 'category')
    search_fields = ('description',)


admin.site.register(Entry, EntryAdmin)
