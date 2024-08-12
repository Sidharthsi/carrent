# forms.py

# forms.py

from django import forms
from .models import Employee



class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'email', 'phone_number', 'aadhar_number', 'license_number', 'front_license_image', 'back_license_image', 'dob', 'gender', 'password', 'joining_date', 'salary']

# forms.py

from django import forms
from .models import Car1

class CarRegistrationForm(forms.ModelForm):
    class Meta:
        model = Car1
        fields = '__all__'  # You may want to specify the fields explicitly instead of '__all__'
from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
from django import forms
from .models import Package

class PackageUpdateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [  'condition', 'number_of_days', 'package_price']
        # Include all fields that you want to update in the form
from django import forms
from .models import CarPackageBooking

class CarPackageBookingForm(forms.ModelForm):
    class Meta:
        model = CarPackageBooking
        fields = '__all__'  # Use all fields from the CarPackageBooking model
