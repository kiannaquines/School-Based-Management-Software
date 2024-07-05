from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.query import QuerySet

class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN_USER = "ADMIN",'ADMIN'
        CHAIRPERSON = "CHAIRPERSON",'CHAIRPERSON'
        MEMBER = "MEMBER",'MEMBER'
        KPI = "KPI TEAM",'KPI TEAM'
        SBM_COORDINATOR = "SBM COORDINATOR",'SBM COORDINATOR'

    BASE_ROLE = Role.ADMIN_USER

    user_gender  = models.CharField(choices=(('1','Male'),('2','Female')),max_length=255,null=True,default="",blank=True)
    user_mobile  = models.CharField(max_length=150,help_text="Enter your mobile number",null=True,blank=True)
    user_profile = models.FileField(upload_to="profile/",null=True,blank=True,default="profile/default.jpg")
    user_role    = models.CharField(choices=Role.choices,max_length=30,default=BASE_ROLE)
    middle_name  = models.CharField(max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class MemberUserManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs) -> QuerySet:
        results = super().get_queryset(*args,**kwargs)
        return results.filter(user_role=User.Role.MEMBER) 
    

class MemberUser(User):
    BASE_ROLE = User.Role.MEMBER
    principle_leader = MemberUserManager()

    def save(self,*args,**kwargs):
        if not self.pk:
            self.is_active = False
            self.user_role = self.BASE_ROLE
            return super().save(*args,**kwargs)

    class Meta:
        proxy = True

class CharipersonUserManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs) -> QuerySet:
        results = super().get_queryset(*args,**kwargs)
        return results.filter(user_role=User.Role.CHAIRPERSON) 
    

class ChairpersonUser(User):
    BASE_ROLE = User.Role.CHAIRPERSON
    principle_leader = CharipersonUserManager()

    def save(self,*args,**kwargs):
        if not self.pk:
            self.is_active = False
            self.user_role = self.BASE_ROLE
            return super().save(*args,**kwargs)

    class Meta:
        proxy = True

