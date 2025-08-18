from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagementProxy(User):
    """
    Proxy model for User Management admin interface.
    This allows us to create a custom admin interface without
    conflicting with Django's default User admin.
    """
    class Meta:
        proxy = True
        verbose_name = 'User Management'
        verbose_name_plural = 'User Management' 