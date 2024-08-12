
from django.db import models

class CarRentalBookings(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    license_number = models.CharField(max_length=20, null=True, default=None)
    front_license_image = models.ImageField(upload_to='license_images/', null=True, default=None)
    back_license_image = models.ImageField(upload_to='license_images/', null=True, default=None)
    pickup_date = models.DateField()
    pickup_time = models.CharField(max_length=8)  # Changed to CharField
    return_date = models.DateField(null=True, blank=True)  # New field for return date
    return_time = models.CharField(max_length=8, null=True, blank=True)  # New field for return time
    work_status = models.CharField(max_length=20,default='Pending')
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    DRIVER_CHOICES = [
        ('driver', 'Driver'),
        ('self_driver', 'Self Driver'),
    ]
    driver_choice = models.CharField(max_length=11, choices=DRIVER_CHOICES, default='self_driver')
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    
    car_id = models.PositiveIntegerField(blank=True, null=True)
    employee_id = models.PositiveIntegerField(default=0)  # Set default value to 0
    duration_unit = models.CharField(max_length=20, default='hours')  # Unit of rental duration
    rental_duration = models.IntegerField()  # Rental duration in hours

  



# models.py

from django.db import models
from django.utils import timezone

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    license_number = models.CharField(max_length=20)
    front_license_image = models.ImageField(upload_to='license_images/')
    back_license_image = models.ImageField(upload_to='license_images/')
    dob = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Trans', 'Trans'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    password = models.CharField(max_length=50)
    joining_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Set a default value for salary


    def __str__(self):
        return self.full_name


# car_reg model 
    
# models.py

from django.db import models

from django.db import models

class Car1(models.Model):
    car_photo = models.ImageField(upload_to='car_photos')
    car_photo_2 = models.ImageField(upload_to='car_photos', blank=True, null=True)
    car_photo_3 = models.ImageField(upload_to='car_photos', blank=True, null=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    transmission_type = models.CharField(max_length=20, choices=[('automatic', 'Automatic'), ('manual', 'Manual')])
    seat_number = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')])
    availability = models.CharField(max_length=20, choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    condition = models.CharField(max_length=20, choices=[('excellent', 'Excellent'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')])
    additional_features = models.CharField(max_length=100)
    description = models.TextField()
    hour_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    day_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car_make} {self.car_model} ({self.vehicle_number})'


from django.db import models

class CarReservation(models.Model):
    pickup_date = models.DateField()
    pickup_time = models.CharField(max_length=8)  # Changed to CharField
    return_date = models.DateField()
    return_time = models.CharField(max_length=8)  # Changed to CharField
    duration_unit = models.CharField(max_length=4, choices=[('hour', 'Hour(s)'), ('day', 'Day(s)')], default='hour')
    rental_duration = models.IntegerField(default=0)  # Default value for rental duration

    # Other fields and methods if any

from django.db import models

class Package(models.Model):
    package_name = models.CharField(max_length=100)
    car_photo = models.ImageField(upload_to='car_photos')
    car_photo_2 = models.ImageField(upload_to='car_photos', blank=True, null=True)
    car_photo_3 = models.ImageField(upload_to='car_photos', blank=True, null=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    transmission_type = models.CharField(max_length=20, choices=[('automatic', 'Automatic'), ('manual', 'Manual')])
    seat_number = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')])
    availability = models.CharField(max_length=20, choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    condition = models.CharField(max_length=20, choices=[('excellent', 'Excellent'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')])
    additional_features = models.CharField(max_length=100)
    description = models.TextField()
    number_of_days = models.PositiveIntegerField(default=1)  # Number of days included in the package
    package_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.package_name} - {self.car_make} {self.car_model} ({self.vehicle_number})'
from django.db import models
from datetime import timedelta

class CarPackageBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accept', 'Accepted'),
        ('reject', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    driver_choice = models.CharField(max_length=20, default='self_drive')
    license_number = models.CharField(max_length=50, blank=True, null=True)
    front_license_image = models.ImageField(upload_to='license_images/')
    back_license_image = models.ImageField(upload_to='license_images/')
    pickup_date = models.DateField()
    return_date = models.DateField()
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    number_of_days = models.PositiveIntegerField()  # Number of days included in the package
    package_id = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.full_name} - {self.pickup_date}"

   
from django.db import models

class LastPickup(models.Model):
    pickup_date = models.DateField()

    def __str__(self):
        return str(self.pickup_date)

from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()

    def str(self):
        return self.name