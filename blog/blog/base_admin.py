from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1,IUsed to automatically add articles, categories, tags, sidebars, friend chains, etc Owner field of model
    2,Used to filter the current user's data for queryset
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)