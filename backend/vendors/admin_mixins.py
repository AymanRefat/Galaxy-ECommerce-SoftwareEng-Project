class VendorModelAdminMixin:
    """
    Mixin to restrict an admin model to only show items belonging to the
    currently logged in vendor. Also automatically sets the vendor field
    upon creation.
    """
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'vendor_profile'):
            return qs.filter(vendor=request.user.vendor_profile)
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and 'vendor' in form.base_fields:
            # Remove the vendor field from the form for vendors
            del form.base_fields['vendor']
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'vendor_profile'):
            # Automatically assign the vendor profile
            obj.vendor = request.user.vendor_profile
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and hasattr(request.user, 'vendor_profile'):
            return getattr(obj, 'vendor', None) == request.user.vendor_profile
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and hasattr(request.user, 'vendor_profile'):
            return getattr(obj, 'vendor', None) == request.user.vendor_profile
        return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and hasattr(request.user, 'vendor_profile'):
            return getattr(obj, 'vendor', None) == request.user.vendor_profile
        return True
