

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('',views.contact_me,name="contactme"),
    path('home.html',views.home,name="instruction"),
    path('Products.html',views.products,name="products"),
    path('Instruction.html',views.instruction,name="instuction"),
    path('Automate.html',views.automate,name="automate"),
    path('One_bulk.html',views.One_bulk,name="one_bulk"),
    path('excel_process',views.Excel_Process,name="excel_process"),
    path('variable_count',views.variable_count,name="variable_count")
    # path('multiple',views.multiple_upload,name="excel_process"),
]
