def add_root_url_to_template(request):
    from django.conf import settings
    return {"dynsite_root": settings.DYNSITE_ROOT}
