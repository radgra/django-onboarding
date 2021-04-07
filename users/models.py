from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from image_cropping import ImageRatioField

class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.username

class Profile(models.Model):
    MALE = 'ML'
    FEMALE = 'FM'
    GENDER_CHOICES = (
        (MALE,'Male'),
        (FEMALE, 'Female')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    short_code = models.CharField(max_length=3,null=True, unique=True) # cool - allow null but doesnt allow blank on staff form(not new mitarbeiter)
    email = models.EmailField(null=True) #iwerken email ,  same as previous one
    user = models.OneToOneField(get_user_model(),null=True,blank=True, on_delete=models.CASCADE)
    # gender choices fields
    picture = models.ImageField(upload_to="profile_pics", null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE)
    cropping = ImageRatioField('picture', '300x300')

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'