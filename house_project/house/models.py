from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'seller'),
        ('buyer', 'buyer')
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='buyer')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)


class Property(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=50)
    PROPERTY_CHOICES = (
        ('Квартира', 'Квартира'),
        ('Дом', 'Дом'),
        ('Участок', 'Участок'),
        ('Гараж', 'Гараж'),
        ('Дача', 'Дача'),
        ('Коммерческая недвижимость', 'Коммерческая недвижимость'),
        ('Комната', 'Комната'),
    )
    property_type = models.CharField(max_length=100, choices=PROPERTY_CHOICES, default='Квартира')
    street = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    ROOMS_CHOICES = (
        ('1-ком', '1-ком'),
        ('2-ком', '2-ком'),
        ('3-ком', '3-ком'),
        ('4-ком', '4-ком'),
        ('5-ком', '5-ком'),
        ('6-и больше ком', '6-и больше ком'),
        ('Свободная планировка', 'Свободная планировка')
    )
    rooms = models.CharField(max_length=32, choices=ROOMS_CHOICES)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 20)], null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 20)], null=True, blank=True)
    CONDITION_CHOICES = [
        ('без отделки', 'Без отделки'),
        ('черновая', 'Черновая отделка'),
        ('косметика', 'Косметический ремонт'),
        ('евро', 'Евроремонт'),
        ('дизайнерский', 'Дизайнерский ремонт'),
        ('требуется', 'Требуется ремонт'),
    ]

    condition = models.CharField(max_length=32, choices=CONDITION_CHOICES, default='черновая')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Region(models.Model):
    name = models.CharField(max_length=54)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='regions', null=True, blank=True)

class City(models.Model):
    name = models.CharField(max_length=54)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='cities', null=True, blank=True)

class District(models.Model):
    name = models.CharField(max_length=54)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='districts', null=True, blank=True)


class LegalDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')


class HouseImage(models.Model):
    image = models.ImageField(upload_to='house_images/')
    house_image = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='image_house')



class HouseReview(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_review')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property} - {self.author}'




class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author_review')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_review')
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.author} - {self.seller}'

class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')


class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('approved', 'Подтверждено'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rentals')
    renter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='renter_rentals')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)