from django.contrib import admin
from expenses.models import (
        Currency,
        AccountGroup, Account,
        Entry, EntryComponent, EntryComment, EntryCategory)


admin.site.register(Currency)
admin.site.register(AccountGroup)
admin.site.register(Account)

admin.site.register(EntryCategory)


class EntryComponentInline(admin.TabularInline):
    model = EntryComponent
    extra = 2


class EntryCommentInline(admin.TabularInline):
    model = EntryComment
    extra = 1


class EntryAdmin(admin.ModelAdmin):
    inlines = [
            EntryComponentInline,
            EntryCommentInline]

    date_hierarchy = "valid_date"

    list_filter = ('creator', 'category')
    search_fields = ('description',)

admin.site.register(Entry, EntryAdmin)
