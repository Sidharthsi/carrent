from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CarRentalBookings, Car1
from twilio.rest import Client
from django.conf import settings
from datetime import date,timedelta

# Home view
def home(request):
    return render(request,'home.html')

# Admin login view
admin_username = "admin"
admin_password = "admin"
# views.py

from django.shortcuts import render
from .models import Car1  # Import your Car model

def explore_cars(request):
    cars = Car1.objects.all()  # Query all cars
    return render(request, 'explore.html', {'cars': cars})

def admin_login(request):
    error = None
    if request.method == "POST":
        entered_username = request.POST.get('username')
        entered_password = request.POST.get('password')

        if entered_username == admin_username and entered_password == admin_password:
            request.session['admin'] = True
            return redirect('admin_home')
        else:
            error = "Login failed. Please check your username and password."
    
    return render(request, 'admin_login.html', {'error': error})

# Admin home view
def admin_home(request):
    if not request.session.get('admin'):
        return redirect('admin_login')
    
    return render(request, 'admin_home.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Car1, CarRentalBookings
from datetime import datetime
from django.http import HttpResponseBadRequest  # Import HttpResponseBadRequest


def rent_car(request, car_id):
    car = get_object_or_404(Car1, id=car_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        return_date = request.POST.get('return_date')  
        return_time = request.POST.get('return_time')  
        driver_choice = request.POST.get('driver_choice')
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        license_number = request.POST.get('license_number')
        work_status = request.POST.get('work_status') 
        rental_duration_days = request.POST.get('rental_duration_days')
        rental_duration_hours = request.POST.get('rental_duration_hours')
        duration_unit = request.POST.get('duration_unit', 'hours')  # Defaulting to 'hours'
        rental_duration= request.POST.get('rental_duration')
        



        try:
            pickup_time = datetime.strptime(pickup_time, '%I:%M %p').strftime('%I:%M %p')
            return_time = datetime.strptime(return_time, '%I:%M %p').strftime('%I:%M %p')  
            # Parse pickup and return dates
            pickup_date = datetime.strptime(pickup_date, '%B %d, %Y').strftime('%Y-%m-%d')
            return_date = datetime.strptime(return_date, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError:
            return HttpResponse("Invalid date or time format.")

       
        front_license_image = request.FILES.get('front_license_image')
        back_license_image = request.FILES.get('back_license_image')

        employee_id = request.POST.get('employee_id', '0')  # Defaulting to 0 if not provided

        booking = CarRentalBookings.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            aadhar_number=aadhar_number,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            return_date=return_date,  
            return_time=return_time,  
            driver_choice=driver_choice,
            from_location=from_location,
            to_location=to_location,
            license_number=license_number, 
            work_status='Pending',  
            duration_unit=duration_unit,
            rental_duration=rental_duration,
            car_id=car_id,
            employee_id=employee_id,
            front_license_image=front_license_image,
            back_license_image=back_license_image
            
        )

        return render(request, 'success.html')

    else:
        today = date.today()
        return render(request, 'book_car.html', {'today': today, 'car': car})


# Car rental bookings view
# Car rental bookings view
from .models import CarRentalBookings, Employee

def car_rental_bookings(request):
    pending_bookings = CarRentalBookings.objects.filter(status='Pending')
    accepted_bookings = CarRentalBookings.objects.filter(status='Accepted', driver_choice__in=['self_driver', 'driver'])
    rejected_bookings = CarRentalBookings.objects.filter(status='Rejected')
    
    # Filter bookings where employee_id is not equal to 0
    assigned_employees = CarRentalBookings.objects.exclude(employee_id=0)

    # Fetch employee full names using employee_ids
    for booking in assigned_employees:
        try:
            employee = Employee.objects.get(pk=booking.employee_id)
            booking.fullname = employee.full_name
        except Employee.DoesNotExist:
            booking.fullname = "N/A"

    return render(request, 'booking_list.html', {
        'pending_bookings': pending_bookings,
        'accepted_bookings': accepted_bookings,
        'rejected_bookings': rejected_bookings,
        'driver_bookings': accepted_bookings.filter(driver_choice='driver', employee_id=0),
        'self_driver_bookings': accepted_bookings.filter(driver_choice='self_driver'),
        'assigned_employees': assigned_employees,  # Pass assigned employees data to the template
    })


# Booking details view
from django.shortcuts import render, get_object_or_404
from .models import CarRentalBookings, Car1

def booking_details(request, booking_id):
    booking = get_object_or_404(CarRentalBookings, pk=booking_id)

    # Fetch the corresponding car details using the car_id from the booking
    car_id = booking.car_id
    car = get_object_or_404(Car1, pk=car_id)

    if request.method == 'POST':
        if 'accept' in request.POST:
            booking.status = 'Accepted'
            booking.save()
            return redirect('car_rental_bookings')  # Redirect back to the booking list page
        elif 'reject' in request.POST:
            booking.status = 'Rejected'
            booking.save()
            return redirect('car_rental_bookings')  # Redirect back to the booking list page

    return render(request, 'booking_details.html', {'booking': booking, 'car': car,})


# Employee form view


# views.py

from django.shortcuts import render, redirect
from .forms import EmployeeRegistrationForm

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee.html', {'form': form})

#login for staff
# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee

def staff_home(request):
    # Implement your staff home view logic here
    return render(request, 'staff_home.html')

def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        input_password = request.POST.get('password')

        try:
            # Retrieve the employee based on the provided email and password
            employee = Employee.objects.get(email=email, password=input_password)
            request.session['employee_id'] = employee.id  # Store the employee ID in the session
            return redirect('staff_home')  # Redirect to the staff home page if login is successful
        except Employee.DoesNotExist:
            # If no employee with the provided credentials is found, display an error message
            messages.error(request, 'Login failed. Please check your email and password.')

    # Render the staff login page
    return render(request, 'staff_login.html')
def staff_profile(request):
    # Your view logic here
    pass

def employee_details(request):
    if 'employee_id' not in request.session:
        return redirect('staff_login')

    employee_id = request.session['employee_id']
    employee = Employee.objects.get(pk=employee_id)


    return render(request, 'employee_details.html', {'employee': employee})


#


from django.shortcuts import render
from .models import Employee

def staff_profile(request):
    # Retrieve employee data from the database
    if 'employee_id' in request.session:
        employee_id = request.session['employee_id']
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            employee = None

        if employee:
            context = {
                'employee': employee
            }
            return render(request, 'staff_profile.html', context)
        else:
            # Handle case where employee does not exist
            return render(request, 'error.html', {'message': 'Employee not found'})
    else:
        # Handle case where employee_id is not in session
        return render(request, 'error.html', {'message': 'Session data not found'})

from django.shortcuts import render, HttpResponse
from .models import CarRentalBookings, Employee
from twilio.rest import Client
from django.conf import settings
from django.http import Http404

def send_sms(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        message = request.POST.get('message')
        description = request.POST.get('description')
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')

        if booking_id and message and description and phone_number and full_name:
            try:
                # Construct the message with booking details
                full_message = f"Hello {full_name},\n\n{message}\n\nDescription: {description}"
                
                # Initialize Twilio client
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                
                # Send SMS
                client.messages.create(
                    body=full_message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                
                return HttpResponse("SMS sent successfully")
            except Exception as e:
                return HttpResponse(f"Failed to send SMS. Error: {str(e)}")
        else:
            return HttpResponse("Missing required fields for sending SMS")
    else:
        booking_id = request.GET.get('booking_id')
        if booking_id:
            try:
                booking = CarRentalBookings.objects.get(pk=booking_id)
                
                try:
                    employee = Employee.objects.get(pk=booking.employee_id)
                    return render(request, 'send_sms.html', {'booking': booking, 'employee': employee})
                except Employee.DoesNotExist:
                    # Handle case where Employee is not found
                    return render(request, 'send_sms.html', {'booking': booking, 'employee_not_found': True})
                
            except CarRentalBookings.DoesNotExist:
                return HttpResponse("Booking ID does not exist.")
        else:
            return HttpResponse("No booking ID provided.")


# registration 
# views.py

# views.py

from django.shortcuts import render
from django.http import HttpResponse
from .forms import CarRegistrationForm

def register_car(request):
    if request.method == 'POST':
        form = CarRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data here
            # Save the form data to the database, etc.
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = CarRegistrationForm()
    return render(request, 'car_reg.html', {'form': form})
# car views.py
from django.shortcuts import render
from .models import Car1

def car_list(request):
  # Filter cars by availability
  available_cars = Car1.objects.filter(availability='available')
  return render(request, 'car_list.html', {'cars': available_cars})



# detail views.py

from django.shortcuts import render, get_object_or_404
from .models import Car1

def car_detail(request, car_id):
    car = get_object_or_404(Car1, pk=car_id)
    return render(request, 'detail.html', {'car': car})
#

from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Car1, CarRentalBookings

def parse_time_str(time_str):
    # Try to parse time string with AM/PM format
    try:
        return datetime.strptime(time_str, '%I:%M %p').time()
    except ValueError:
        pass
    
    # Try to parse time string in 24-hour format
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        raise ValueError(f"Unsupported time format: {time_str}")
from django.shortcuts import render
from datetime import datetime, timedelta
from django.db.models import Q
from .models import CarRentalBookings, CarReservation, Car1

def availability_check(request):
    if request.method == 'POST':
        try:
            # Get form data
            pickup_date = datetime.strptime(request.POST.get('pickup_date'), '%Y-%m-%d').date()
            pickup_time = datetime.strptime(request.POST.get('pickup_time'), '%H:%M').time()  # Parse as 24-hour format
            rental_duration = int(request.POST.get('rental_duration'))
            duration_option = request.POST.get('duration_option')

            # Calculate pickup datetime
            pickup_datetime = datetime.combine(pickup_date, pickup_time)

            # Calculate return datetime based on rental duration
            if duration_option == 'hour':
                return_datetime = pickup_datetime + timedelta(hours=rental_duration)
                duration_unit = 'hour'
            elif duration_option == 'day':
                return_datetime = pickup_datetime + timedelta(days=rental_duration)
                duration_unit = 'day'
            else:
                raise ValueError("Invalid duration option")

            # Query conflicting bookings
            conflicting_bookings = CarRentalBookings.objects.filter(
                Q(
                    Q(return_date__gt=pickup_datetime) |
                    (Q(return_date=pickup_datetime.date()) & Q(return_time__gt=pickup_datetime.time()))
                ) &
                Q(
                    Q(pickup_date__lt=return_datetime) |
                    (Q(pickup_date=return_datetime.date()) & Q(pickup_time__lt=return_datetime.time()))
                )
            ).exclude(status='Rejected')

            # Get available cars
            available_cars = Car1.objects.filter(availability='available').exclude(id__in=conflicting_bookings.values_list('car_id', flat=True))

            if not available_cars:
                # No cars available for this date and time
                return render(request, 'no_cars_available.html', {'pickup_date': pickup_date, 'pickup_time': pickup_time})

            # Create a CarReservation object
            reservation = CarReservation(
                pickup_date=pickup_date,
                pickup_time=pickup_time.strftime('%I:%M %p'),  # Format as 1:00 PM
                return_date=return_datetime.date(),
                return_time=return_datetime.strftime('%I:%M %p'),  # Format as 1:00 PM
                duration_unit=duration_unit,
                rental_duration=rental_duration
            )

            # Save the reservation to the database
            reservation.save()

            # Render template with available cars
            return render(request, 'car_list.html', {'cars': available_cars})

        except Exception as e:
            # Handle any exceptions and render error page
            return render(request, 'error.html', {'error_message': str(e)})

    return render(request, 'availability_check.html')


from django.http import JsonResponse
from .models import CarReservation
from datetime import datetime

def fetch_last_reservation_data(request):
    try:
        # Retrieve the last reservation data from the CarReservation model
        last_reservation = CarReservation.objects.order_by('-id').first()

        if last_reservation:
            # Format pickup and return times with AM/PM
            pickup_time = datetime.strptime(last_reservation.pickup_time, '%I:%M %p').strftime('%I:%M %p')
            return_time = datetime.strptime(last_reservation.return_time, '%I:%M %p').strftime('%I:%M %p')

            # Create a dictionary containing the last reservation data
            data = {
                'pickup_date': last_reservation.pickup_date.strftime('%B %d, %Y'),
                'pickup_time': pickup_time,
                'return_date': last_reservation.return_date.strftime('%B %d, %Y'),
                'return_time': return_time,
                'duration_unit': last_reservation.duration_unit,  # Include duration_unit
                'rental_duration': last_reservation.rental_duration,  # Include rental_duration
            }

            # Return the data as JSON response
            return JsonResponse(data)
        else:
            # Handle case where no reservation exists
            return JsonResponse({'error': 'No reservation found'}, status=404)

    except Exception as e:
        # Handle any exceptions and return an error response
        return JsonResponse({'error': str(e)}, status=500)



#
def assign_employee_view(request, booking_id):
    booking = get_object_or_404(CarRentalBookings, pk=booking_id)
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        
        if employee_id:
            try:
                employee = Employee.objects.get(pk=employee_id)
                
                # Check if the selected employee is already assigned to another pending booking
                conflicting_booking = CarRentalBookings.objects.filter(employee_id=employee_id, status='Pending').exclude(pk=booking_id).first()
                if conflicting_booking:
                    return render(request, 'error.html', {'message': 'Selected employee is already assigned to another pending booking.'})
                
                # Check if the employee has any work on the day of the booking
                existing_booking_on_day = CarRentalBookings.objects.filter(employee_id=employee_id, pickup_date=booking.pickup_date).exclude(pk=booking_id).first()
                if existing_booking_on_day:
                    return render(request, 'error.html', {'message': 'Selected employee already has work on the day of this booking.'})
                
                # Check if the employee's existing work overlaps with the new booking
                conflicting_booking_on_day = CarRentalBookings.objects.filter(
                    employee_id=employee_id,
                    pickup_date=booking.pickup_date,
                    return_date=booking.return_date,
                    pickup_time__lt=booking.return_time,
                    return_time__gt=booking.pickup_time
                ).exclude(pk=booking_id).first()
                if conflicting_booking_on_day:
                    return render(request, 'error.html', {'message': 'Selected employee already has work overlapping with this booking.'})

                # Update the booking with the selected employee
                booking.employee = employee
                booking.employee_id = employee_id
                booking.save()

                messages.success(request, 'Employee assigned successfully.')

                return redirect('car_rental_bookings')
            
            except Employee.DoesNotExist:
                return render(request, 'error.html', {'message': 'Selected employee does not exist.'})
    
    # Fetch all available employees
    employees = Employee.objects.all()
    
    # Filter out employees who have existing work on the day of the booking or who are already assigned to another pending booking
    employees = employees.exclude(
        id__in=CarRentalBookings.objects.filter(status='Pending').values_list('employee_id', flat=True)
    ).exclude(
        id__in=CarRentalBookings.objects.filter(pickup_date=booking.pickup_date).values_list('employee_id', flat=True)
    )
    
    return render(request, 'allotment.html', {'booking': booking, 'employees': employees})

# reassihn
# views.py
# views.py
def reassign_employee_view(request, booking_id):
    booking = get_object_or_404(CarRentalBookings, pk=booking_id)
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        
        if employee_id:
            try:
                employee = Employee.objects.get(pk=employee_id)
                
                # Check if the selected employee is already assigned to another pending booking
                conflicting_booking = CarRentalBookings.objects.filter(employee_id=employee_id, status='Pending').exclude(pk=booking_id).first()
                if conflicting_booking:
                    return render(request, 'error.html', {'message': 'Selected employee is already assigned to another pending booking.'})
                
                # Check if the employee has any work on the day of the booking
                existing_booking_on_day = CarRentalBookings.objects.filter(employee_id=employee_id, pickup_date=booking.pickup_date).exclude(pk=booking_id).first()
                if existing_booking_on_day:
                    return render(request, 'error.html', {'message': 'Selected employee already has work on the day of this booking.'})
                
                # Check if the employee's existing work overlaps with the new booking
                conflicting_booking_on_day = CarRentalBookings.objects.filter(
                    employee_id=employee_id,
                    pickup_date=booking.pickup_date,
                    return_date=booking.return_date,
                    pickup_time__lt=booking.return_time,
                    return_time__gt=booking.pickup_time
                ).exclude(pk=booking_id).first()
                if conflicting_booking_on_day:
                    return render(request, 'error.html', {'message': 'Selected employee already has work overlapping with this booking.'})

                # Update the booking with the selected employee
                booking.employee = employee
                booking.employee_id = employee_id
                booking.save()

                messages.success(request, 'Employee reassigned successfully.')

                return redirect('car_rental_bookings')
            
            except Employee.DoesNotExist:
                return render(request, 'error.html', {'message': 'Selected employee does not exist.'})
    
    # Fetch all available employees
    employees = Employee.objects.all()
    
    # Filter out employees who have existing work on the day of the booking or who are already assigned to another pending booking
    employees = employees.exclude(
        id__in=CarRentalBookings.objects.filter(status='Pending').values_list('employee_id', flat=True)
    ).exclude(
        id__in=CarRentalBookings.objects.filter(pickup_date=booking.pickup_date).values_list('employee_id', flat=True)
    )
    
    return render(request, 'reallot.html', {'booking': booking, 'employees': employees})

#
from django.shortcuts import render, redirect
from .models import CarRentalBookings

def staff(request):
    if 'employee_id' not in request.session:
        return redirect('staff_home')
    
    employee_id = request.session['employee_id']
    pending_tasks = CarRentalBookings.objects.filter(employee_id=employee_id, work_status='Pending')
    finished_tasks = CarRentalBookings.objects.filter(employee_id=employee_id, work_status='Finished')
    
    # Fetching car_model information from Car1 table for each pending task
    for task in pending_tasks:
        try:
            car1_info = Car1.objects.get(pk=task.car_id)
            task.car_model = car1_info.car_model  # Use car_model instead of model
        except Car1.DoesNotExist:
            task.car_model = "N/A"

    context = {
        'pending_tasks': pending_tasks,
        'finished_tasks': finished_tasks
    }
    return render(request, 'task.html', context)


from django.http import JsonResponse

def finish_task(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')

        try:
            booking = CarRentalBookings.objects.get(pk=booking_id)
            booking.work_status = 'Finished'
            booking.save()
            message = f"Booking ID {booking_id} has been marked as finished successfully."
        except CarRentalBookings.DoesNotExist:
            message = f"Booking ID {booking_id} does not exist."

        return JsonResponse({'message': message})

# views.py
from django.shortcuts import render
from .models import Employee

def employee_management(request):
    employees = Employee.objects.all()
    return render(request, 'staff_detail.html', {'employees': employees})

def about(request):
    return render(request, 'about.html')
# views.py

 # Assuming you have a Booking model in your models.py

from django.shortcuts import render
from .models import CarRentalBookings

from django.shortcuts import render
from .models import CarRentalBookings

from django.shortcuts import render
from .models import CarRentalBookings, Employee

def work_detail(request, employee_id):
    try:
        # Fetch bookings for the employee
        bookings = CarRentalBookings.objects.filter(employee_id=employee_id)

        # Fetch employee's name from the Employee table
        employee_name = Employee.objects.get(id=employee_id).full_name

        # Filter bookings for finished and pending work
        finished_bookings = bookings.filter(work_status="finished")
        pending_bookings = bookings.filter(work_status="Pending")

        context = {
            'finished_bookings': finished_bookings,
            'pending_bookings': pending_bookings,
            'employee_fullname': employee_name,  # Pass the employee's full name to the template
            'employee_id': employee_id
        }
        return render(request, 'work_detail.html', context)
    except CarRentalBookings.DoesNotExist:
        error_message = "No bookings found for this employee."
        return render(request, 'work_detail.html', {'error_message': error_message})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeRegistrationForm

def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_management')  # Redirect to a relevant URL after updating
    else:
        form = EmployeeRegistrationForm(instance=employee)
    
    context = {'form': form, 'employee': employee}  # Include the employee object in the context
    return render(request, 'update_employee.html', context)

################
# views.py
from django.shortcuts import render, get_object_or_404
from .models import CarRentalBookings, Car1

def generate_bill(request):
    # Get the latest booking by querying the database for the booking with the highest ID
    latest_booking = CarRentalBookings.objects.latest('id')
    
    # Retrieve the car details based on the latest booking
    car = get_object_or_404(Car1, pk=latest_booking.car_id)
    
    # Calculate rental cost based on duration and unit
    if latest_booking.duration_unit == 'hour':
        total_cost = latest_booking.rental_duration * car.hour_price
    elif latest_booking.duration_unit == 'day':
        total_cost = latest_booking.rental_duration * car.day_price
    else:
        total_cost = 0  # Handle unexpected duration unit here
    
    # Prepare context data to pass to the bill.html template
    context = {
        'booking': latest_booking,
        'car': car,
        'total_cost': total_cost
    }
    
    # Render bill.html with the context data
    return render(request, 'bill.html', context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # Import for converting HTML to PDF

def render_bill_pdf(request, booking_id):
    # Retrieve booking and car details
    booking = get_object_or_404(CarRentalBookings, pk=booking_id)
    car = get_object_or_404(Car1, pk=booking.car_id)

    # Calculate total cost based on duration and unit
    if booking.duration_unit == 'hour':
        total_cost = booking.rental_duration * car.hour_price
    elif booking.duration_unit == 'day':
        total_cost = booking.rental_duration * car.day_price
    else:
        total_cost = 0  # Handle unexpected duration unit here

    context = {
        'booking': booking,
        'car': car,
        'total_cost': total_cost
    }

    # Render bill template as HTML
    template = get_template('bill.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rental_bill.pdf"'

    # Generate PDF from HTML template
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
####

# views.py

from django.shortcuts import render
from .models import Car1

def car_management(request):
    cars = Car1.objects.all()
    return render(request, 'car_management.html', {'cars': cars})
from django.shortcuts import render, get_object_or_404
from .models import Car1

def car_details(request, car_id):
    car = get_object_or_404(Car1, pk=car_id)
    return render(request, 'car_detail.html', {'car': car})
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Car1

def update_car(request, car_id):
    car = get_object_or_404(Car1, pk=car_id)

    if request.method == 'POST':
        # Update car details based on form submission
        car.hour_price = request.POST.get('hour_price')
        car.day_price = request.POST.get('day_price')
        car.availability = request.POST.get('availability')
        car.save()
        return redirect('car_management')  # Redirect to admin home after update

    # Render update form with existing car details
    return render(request, 'update_car.html', {'car': car})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Car1

@csrf_exempt
def update_availability(request, car_id):
    if request.method == 'POST':
        # Retrieve the car object from the database
        car = get_object_or_404(Car1, pk=car_id)

        # Toggle the availability status
        if car.availability == 'available':
            car.availability = 'unavailable'
        else:
            car.availability = 'available'
        
        # Save the updated availability
        car.save()

        # Return JSON response with updated availability status
        return JsonResponse({'availability': car.availability})
    else:
        # Handle invalid request method (GET or other methods)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
# views.py
from django.shortcuts import render, redirect
from .models import Package
from .forms import PackageForm

def register_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'pack_reg.html', {'form': form})

from django.shortcuts import render
from .models import Package  # Import the Package model

def package_list(request):
    packages = Package.objects.filter(availability='available')  # Fetch available packages
    return render(request, 'package_list.html', {'packages': packages})
#####################
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Package

def package_management(request):
    packages = Package.objects.all()  # Retrieve all packages
    return render(request, 'package_management.html', {'packages': packages})
###############
from django.shortcuts import render, redirect
from .models import Package
from .forms import PackageUpdateForm  # Import your Package update form here
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package
from .forms import PackageUpdateForm  # Import your PackageUpdateForm from forms.py

def update_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)

    if request.method == 'POST':
        form = PackageUpdateForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('package_management')  # Redirect to admin home after update
    else:
        form = PackageUpdateForm(instance=package)
    
    return render(request, 'update_package.html', {'form': form, 'package': package})
############
from django.shortcuts import render, get_object_or_404
from .models import Package

def package_details(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'package_detail.html', {'package': package})
#############
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import CarPackageBooking, Package
from datetime import datetime, timedelta

@csrf_exempt  # Use this decorator to exempt CSRF protection for this view (not recommended for production)
def car_booking(request):
    if request.method == 'POST':
        # Extract data from POST request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        license_number = request.POST.get('license_number')
        front_license_image = request.FILES.get('front_license_image')
        back_license_image = request.FILES.get('back_license_image')
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        package_id = request.POST.get('package_id')
        number_of_days = request.POST.get('number_of_days')

        # Process date strings into datetime objects
        pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_date = datetime.strptime(return_date, '%Y-%m-%d')

        # Save booking details to the database
        booking = CarPackageBooking(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            aadhar_number=aadhar_number,
            license_number=license_number,
            front_license_image=front_license_image,
            back_license_image=back_license_image,
            pickup_date=pickup_date,
            return_date=return_date,
            from_location=from_location,
            to_location=to_location,
            number_of_days=number_of_days,
            package_id=package_id
        )
        booking.save()

        # Redirect to a success page or render a success template
        return render(request, 'booking_success.html')

    else:
        # Handle GET request (not necessary for form submission)
        return render(request, 'book_pack.html')
# views.py

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import CarPackageBooking, Package
from datetime import datetime

def car_booking(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    initial_data = {
        'number_of_days': package.number_of_days,
        'package_id': package_id
    }

    if request.method == 'POST':
        # Retrieve form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        license_number = request.POST.get('license_number')
        front_license_image = request.FILES.get('front_license_image')
        back_license_image = request.FILES.get('back_license_image')
        pickup_date_str = request.POST.get('pickup_date')
        return_date_str = request.POST.get('return_date')
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        number_of_days = request.POST.get('number_of_days')

        # Validate and parse dates
        try:
            if pickup_date_str:
                pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
            else:
                raise ValueError("Pickup date is missing")

            if return_date_str:
                return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
            else:
                raise ValueError("Return date is missing")
        except (ValueError, TypeError) as e:
            return render(request, 'booking_error.html', {'error_message': str(e)})

        # Create CarPackageBooking instance
        booking = CarPackageBooking(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            aadhar_number=aadhar_number,
            license_number=license_number,
            front_license_image=front_license_image,
            back_license_image=back_license_image,
            pickup_date=pickup_date,
            return_date=return_date,
            from_location=from_location,
            to_location=to_location,
            number_of_days=number_of_days,
            package_id=package_id
        )

        try:
            # Save the booking instance
            booking.save()
            return render(request, 'booking_success.html')
        except Exception as e:
            return render(request, 'booking_error.html', {'error_message': str(e)})

    # If not a POST request or form data missing, render the form
    return render(request, 'book_pack.html', {'package': package, 'initial_data': initial_data})

from django.shortcuts import render
from .models import Package, CarPackageBooking, LastPickup
from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest

def pack_availability(request):
    if request.method == 'GET' and 'pickup_date' in request.GET:
        pickup_date_str = request.GET.get('pickup_date')

        try:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
            
            LastPickup.objects.create(pickup_date=pickup_date)  # Store the last pickup date

            number_of_days = int(request.GET.get('number_of_days', 1))
            return_date = pickup_date + timedelta(days=number_of_days)

            conflicting_bookings = CarPackageBooking.objects.filter(
                return_date__gt=pickup_date,
                pickup_date__lt=return_date
            ).exclude(status='rejected')

            conflicting_package_ids = set(conflicting_bookings.values_list('package_id', flat=True))

            available_packages = Package.objects.filter(
                availability='available'
            ).exclude(
                id__in=conflicting_package_ids
            )

            return render(request, 'package_list.html', {
                'available_packages': available_packages,
                'pickup_date': pickup_date_str,
                'number_of_days': number_of_days
            })
        except ValueError:
            return render(request, 'package_list.html', {'error_message': 'Invalid pickup date'})
    else:
        # Redirect to the form page with an error message
        return render(request, 'pack_avalability.html', {'error_message': 'Invalid request. Please provide a pickup date.'})

from django.http import JsonResponse
from .models import LastPickup

def lastpickup(request):
    # Fetch the last recorded pickup_date from the LastPickup model
    last_pickup = LastPickup.objects.last()

    if last_pickup:
        pickup_date = last_pickup.pickup_date.strftime('%Y-%m-%d')
        return JsonResponse({'pickup_date': pickup_date})
    else:
        return JsonResponse({'pickup_date': None})
# views.py

from django.shortcuts import render
from .models import CarPackageBooking

def car_package_booking_list(request):
    # Retrieve all CarPackageBooking instances
    bookings = CarPackageBooking.objects.all()

    context = {
        'bookings': bookings
    }

    return render(request, 'package_booking.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CarPackageBooking
from django.views.decorators.http import require_POST

@require_POST
def update_booking_status(request, booking_id):
    booking = get_object_or_404(CarPackageBooking, pk=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['accepted', 'rejected']:
            booking.status = new_status
            booking.save()
            return HttpResponse(f'Successfully updated status to {new_status}')
        else:
            return HttpResponse('Invalid status')

    return redirect('/')  # Redirect to some page after processing the form

from django.shortcuts import render
from .models import Feedback

def feedback(request):
    feedback_data = Feedback.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        feedback = request.POST.get('feedbk', '')
        Feedback.objects.create(name=name, email=email, feedback=feedback)

    return render(request, 'feedback.html', {'feedback_data': feedback_data})
from django.shortcuts import render
from .models import Feedback

# Custom function to check if user is admin

def feedback_view(request):
    feedback_data = Feedback.objects.all()
    return render(request, 'admin_feedback.html', {'feedback_data': feedback_data})


from django.shortcuts import render, get_object_or_404
from .models import CarPackageBooking

def packbook_details(request, booking_id):
    booking = get_object_or_404(CarPackageBooking, id=booking_id)
    return render(request, 'packbook_detail.html', {'booking': booking})

# views.py

from django.shortcuts import render
from .models import CarRentalBookings, Employee

def booking_detailing(request):
    if request.method == 'POST':
        # Assuming the form has 'name' and 'email' fields
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Get all bookings associated with the provided email
        bookings = CarRentalBookings.objects.filter(full_name=name, email=email)

        # Create a list to store booking details with employee names
        booking_details = []

        for booking in bookings:
            # Get employee name associated with the booking's employee_id
            employee_name = ""
            if booking.employee_id != 0:
                employee = Employee.objects.filter(id=booking.employee_id).first()
                if employee:
                    employee_name = employee.full_name

            # Append booking details along with employee name to the list
            booking_details.append({
                'booking': booking,
                'employee_name': employee_name
            })

        return render(request, 'user_show.html', {'booking_details': booking_details})

    return render(request, 'user_booked.html')  # Render form template for entering name and email
from django.shortcuts import render
from .models import CarPackageBooking

def user_packdetails(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        
        # Retrieve all bookings for the specified email and full_name
        bookings = CarPackageBooking.objects.filter(email=email, full_name=full_name)
        
        # Render the template with the list of bookings
        return render(request, 'user_packbook.html', {'bookings': bookings, 'email': email, 'full_name': full_name})
    else:
        return render(request, 'user_pack.html')
