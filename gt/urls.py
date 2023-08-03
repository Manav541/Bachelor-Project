"""gt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gt_admin import views
from gt_client import client_views
from django.conf.urls import url
from gt_admin.views import HomeView, ProjectChart

urlpatterns = [
    # --------Show Data Dictionary----------(select * from tablename)
    path('admin/', admin.site.urls),
    path('user_table/', views.user_table),
    path('category_table/', views.category_table),
    path('subcategory_table/', views.subcategory_table),
    path('product_table/', views.product_table),
    path('gallery_table/', views.gallery_table),
    path('cart_table/', views.cart_table),
    path('order_table/', views.order_table),
    path('order_item_table/', views.order_item_table),
    path('payment_table/', views.payment_table),
    path('feedback_table/', views.feedback_table),
    path('contactus_table/', views.contact_us_table),

    # --------Delete Data From Database----------(delete * from tablename)
    path('delete_category/<int:id>', views.delete_category),
    path('delete_subcategory/<int:id>', views.delete_subcategory),
    path('delete_product/<int:id>', views.delete_product),
    path('delete_gallery/<int:id>', views.delete_gallery),
    path('delete_cart/<int:id>', views.delete_cart),
    path('delete_order/<int:id>', views.delete_order),
    path('delete_order_item/<int:id>', views.delete_order_item),
    path('delete_payment/<int:id>', views.delete_payment),
    path('delete_feedback/<int:id>', views.delete_feedback),
    path('delete_contact/<int:id>', views.delete_contactus),

    # --------Insert Data From Database----------(insert into tablename values)
    path('insert_category/', views.insert_Category),
    path('insert_subcategory/', views.insert_Subcategory),
    path('insert_product/', views.insert_Product),
    path('insert_gallery/', views.insert_gallery),
    path('insert_cart/', views.insert_Cart),
    path('insert_order/', views.insert_Order),
    path('insert_order_item/', views.insert_Order_Item),
    path('insert_payment/', views.insert_Payment),
    path('insert_feedback/', views.insert_Feedback),
    path('insert_contactus/', views.insert_ContactUs),

    # --------Update Data From Database----------(update tablename set values)
    path('select_category/<int:id>', views.select_category),
    path('update_category/<int:id>', views.update_Category),
    path('select_subcategory/<int:id>', views.select_subcategory),
    path('update_subcategory/<int:id>', views.update_Subcategory),
    path('select_product/<int:id>', views.select_product),
    path('update_product/<int:id>', views.update_Product),
    path('select_order/<int:id>', views.select_order),
    path('update_order/<int:id>', views.update_Order),
    path('select_order_item/<int:id>', views.select_order_item),
    path('update_order_item/<int:id>', views.update_Order_Item),
    path('select_payment/<int:id>', views.select_payment),
    path('update_payment/<int:id>', views.update_Payment),
    path('select_feedback/<int:id>', views.select_feedback),
    path('update_feedback/<int:id>', views.update_Feedback),
    path('select_contactus/<int:id>', views.select_contactus),
    path('update_contactus/<int:id>', views.update_Contactus),

    # --------Login, Forget & Reset Password----------
    path('login/', views.login),
    path('logout/', views.logout),
    path('forget_password/', views.forget_password),
    path('send_otp/', views.sendotp),
    path('reset/', views.set_password),

    # --------Dashboard-Chart & Profile----------
    path('dashboard/', views.dashboard),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
    url(r'charthome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ProjectChart.as_view(), name="api-data"),


    # --------Dashboard-Chart & Profile----------
    path('accepted_order/<int:id>', views.accept_order),
    path('rejected_order/<int:id>', views.rejected_order),

    # ------------------------------------------------CLIENT SIDE-----------------------------------------------------------------------

    path('client/', include('gt_client.client_urls')),
]
