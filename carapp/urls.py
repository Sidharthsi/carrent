from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),  
    path('rent_car/<int:car_id>/', views.rent_car, name='rent_car'),
    path('bookings/', views.car_rental_bookings, name='car_rental_bookings'),
    path('bookings/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('emp/', views.register_employee, name='register_employee'),
    path('send_sms/', views.send_sms, name='send_sms'),
    path('register_car/', views.register_car, name='register_car'),
    path('cars/', views.car_list, name='car_list'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),
    path('availability/',views. availability_check, name='availability_check'),
    path('explore/', views.explore_cars, name='explore_cars'),
    path('assign_employee/<int:booking_id>/', views.assign_employee_view, name='assign_employee'),
    path('reassign_employee/<int:booking_id>/', views.reassign_employee_view, name='reassign_employee'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('staff-home/', views.staff_home, name='staff_home'),
    path('staff-profile/', views.staff_profile, name='staff_profile'),
    path('finish_task/', views.finish_task, name='finish_task'),
    path('staff/', views.staff, name='staff'),
    path('employee_management/', views.employee_management, name='employee_management'),
    path('about/',views.about, name='about'),
    path('work_detail/<int:employee_id>/', views.work_detail, name='work_detail'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('fetch-last-reservation-data/', views.fetch_last_reservation_data, name='fetch_last_reservation_data'),
    path('bill/', views.generate_bill, name='generate_bill'), 
    path('render_bill_pdf/<int:booking_id>/', views.render_bill_pdf, name='render_bill_pdf'),
    path('car_management/', views.car_management, name='car_management'),
    path('car_details/<int:car_id>/', views.car_details, name='car_details'),
    path('update_car/<int:car_id>/', views.update_car, name='update_car'),
    path('update_availability/<int:car_id>/', views.update_availability, name='update_availability'),
    path('register/', views.register_package, name='register_package'),
    path('packages/', views.package_list, name='package_list'), 
    path('package_management/', views.package_management, name='package_management'),
    path('update_package/<int:package_id>/', views.update_package, name='update_package'),
    path('package_details/<int:package_id>/', views.package_details, name='package_details'),    
    path('book-car/<int:package_id>/', views.car_booking, name='book_car'),
    path('pack_availability/', views.pack_availability, name='pack_availability'),
    path('lastpickup/', views.lastpickup, name='lastpickup'),
    path('package_bookings/', views.car_package_booking_list, name='car_package_bookings'),
    path('update_booking_status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('f/', views.feedback, name='feedback'),
    path('packbook_details/<int:booking_id>/',views.packbook_details, name='packbook_details'),
    path('booking_detailing/', views.booking_detailing, name='booking_detailing'),
    path('feedback/', views.feedback_view, name='admin_feedback'),
    path('pack-booking/', views.user_packdetails, name='search_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
