from django.db import models
from django.contrib.auth.models import  AbstractBaseUser ,PermissionsMixin
from api.managers import MyUserManager
#custom user model

class MyUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(("staff status"),
        default=False,
        help_text=(
            "Designates that this user can log into the admin site "

        ))

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','tc'] #required while creating a superuser

    def __str__(self):
        return self.email

    # class Meta:
    #     permissions = (("change_name", "can change name of product"),) # if want to add custom permission
  