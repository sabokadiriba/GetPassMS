from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomizedUser(AbstractUser):
    USER=(
        (1,'SUPERVISER'),
        (2,'EMPLOYEE'),
        (3,'GETKEEPER'),
    )

    user_type = models.CharField(choices = USER,max_length=50,default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
class Project(models.Model):
    name= models.CharField(unique=True, max_length=100 ,default=True)
    def __str__(self):
        return self.name
class GuestRequest(models.Model):
    guest_name= models.TextField(null=True)
    email= models.EmailField( max_length=100 )
    phone= models.CharField( max_length=15 )
    identification_card=models.FileField(null=True)
    date_of_visit= models.DateField()
    purpose_of_visit=models.TextField()
    visit_department=models.TextField()
    arrival_time=models.DateTimeField(null=True)
    departure_time=models.DateTimeField(null=True)
    approval_status=models.CharField(max_length=20 , default='pending')
    feedback=models.TextField(null=True)
    responsible_person=models.TextField(null=True)
    def __str__(self):
        return self.guest_name 
    
class Invitation(models.Model):
    guest_name= models.TextField(null=True)
    email= models.EmailField( max_length=100 )
    phone= models.CharField( max_length=15 )
    purpose_of_visit=models.TextField()
    arrival_date=models.DateTimeField(null=True)
    approval_status=models.CharField(max_length=20 , default='pending')
    feedback=models.TextField(null=True)
    responsible_person=models.TextField(null=True)
    def __str__(self):
        return self.guest_name 
    

class Badge(models.Model):
    badge_id= models.ForeignKey(GuestRequest,on_delete=models.CASCADE)
    issue_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.badge_id.guest_name
class InvitationBadge(models.Model):
    badge_id= models.ForeignKey(Invitation,on_delete=models.CASCADE)
    issue_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.badge_id.guest_name
    
class Department(models.Model):
    department_name= models.TextField()
    def __str__(self):
        return self.department_name
    
class Employee(models.Model):
    customizeduser= models.OneToOneField(CustomizedUser,on_delete=models.CASCADE,related_name='customized_user_groups')
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.customizeduser
