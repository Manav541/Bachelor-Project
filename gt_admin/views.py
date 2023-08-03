import random
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from gt_admin.functions import handle_uploaded_file
from gt_admin.models import user, category, subcategory, product, gallery, cart, order, orderitem, payment, feedback, \
    contactus
from django.shortcuts import render, redirect
from gt_admin.forms import userform, categoryform, subcategoryform, productform, galleryform, cartform, orderform, \
    orderitemform, paymentform, feedbackform, contactusform
import sys
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View


# Create your views here.

# ---------------------------------Show Data Dictionary---------------------------------------
def user_table(request):
    usr = user.objects.all()
    return render(request, "user.html", {'user': usr})


def category_table(request):
    ctg = category.objects.all()
    return render(request, "category.html", {'category': ctg})


def subcategory_table(request):
    sctg = subcategory.objects.all()
    return render(request, "subcategory.html", {'subcategory': sctg})


def product_table(request):
    prdt = product.objects.all()
    return render(request, "product.html", {'product': prdt})


def gallery_table(request):
    glry = gallery.objects.all()
    return render(request, "gallery.html", {'gallery': glry})


def cart_table(request):
    crt = cart.objects.all()
    return render(request, "cart.html", {'cart': crt})


def order_table(request):
    ordr = order.objects.all()
    return render(request, "order.html", {'order': ordr})


def order_item_table(request):
    ordritm = orderitem.objects.all()
    return render(request, "order_item.html", {'orderitem': ordritm})


def payment_table(request):
    pymt = payment.objects.all()
    return render(request, "payment.html", {'payment': pymt})


def feedback_table(request):
    fdbk = feedback.objects.all()
    return render(request, "feedback.html", {'feedback': fdbk})


def contact_us_table(request):
    cntct = contactus.objects.all()
    return render(request, "contact_us.html", {'contactus': cntct})


# ---------------------------------Delete Data---------------------------------------
def delete_category(reqeust, id):
    cat = category.objects.get(category_id=id)
    cat.delete()
    return redirect("/category_table")


def delete_subcategory(reqeust, id):
    subcat = subcategory.objects.get(subcategory_id=id)
    subcat.delete()
    return redirect("/subcategory_table")


def delete_product(reqeust, id):
    prdt = product.objects.get(product_id=id)
    prdt.delete()
    return redirect("/subcategory_table")


def delete_gallery(reqeust, id):
    glry = gallery.objects.get(gallery_id=id)
    glry.delete()
    return redirect("/gallery_table")


def delete_cart(reqeust, id):
    crt = cart.objects.get(cart_id=id)
    crt.delete()
    return redirect("/cart_table")


def delete_order(reqeust, id):
    ordr = order.objects.get(order_id=id)
    ordr.delete()
    return redirect("/order_table")


def delete_order_item(reqeust, id):
    ordr_item = orderitem.objects.get(order_item_id=id)
    ordr_item.delete()
    return redirect("/order_item_table")


def delete_payment(reqeust, id):
    pymt = payment.objects.get(payment_id=id)
    pymt.delete()
    return redirect("/payment_table")


def delete_feedback(reqeust, id):
    fdbk = feedback.objects.get(feedback_id=id)
    fdbk.delete()
    return redirect("/feedback_table")


def delete_contactus(reqeust, id):
    cntkus = contactus.objects.get(contact_id=id)
    cntkus.delete()
    return redirect("/contactus_table")


# ---------------------------------Insert Data---------------------------------------
def insert_Category(request):
    if request.method == "POST":
        form = categoryform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/category_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_category.html', {'form': form})


def insert_Subcategory(request):
    category_records = category.objects.all()
    if request.method == "POST":
        form = subcategoryform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/subcategory_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_subcategory.html', {'form': form, 'category': category_records})


def insert_Product(request):
    subcategory_records = subcategory.objects.all()
    if request.method == "POST":
        form = productform(request.POST, request.FILES)
        print("=====", request.POST.get('product_image'))
        print("-------------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['product_image'])
                form.save()
                return redirect('/product_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = productform()

    return render(request, 'insert_product.html', {'form': form, 'subcategory': subcategory_records})


def insert_gallery(request):
    product_records = product.objects.all()
    if request.method == 'POST':
        g = galleryform(request.POST, request.FILES)
        print('-----------', g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['image_path'])
                g.save()
                return redirect("/gallery_table")
            except:
                print("---------", sys.exc_info())
    else:
        g = galleryform()
        return render(request, "insert_gallery.html", {'form': g, 'product': product_records})


def insert_Cart(request):
    user_records = user.objects.all()
    product_record = product.objects.all()
    if request.method == "POST":
        form = cartform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/cart_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = cartform()

    return render(request, 'insert_cart.html', {'form': form, 'user': user_records, 'product': product_record})


def insert_Order(request):
    user_records = user.objects.all()
    if request.method == "POST":
        form = orderform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/order_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_order.html', {'form': form, 'user': user_records})


def insert_Order_Item(request):
    product_record = product.objects.all()
    order_records = order.objects.all()
    if request.method == "POST":
        form = orderitemform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/order_item_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_order_item.html', {'form': form, 'product': product_record, 'order': order_records})


def insert_Payment(request):
    order_records = order.objects.all()
    if request.method == "POST":
        form = paymentform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/payment_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_payment.html', {'form': form, 'order': order_records})


def insert_Feedback(request):
    user_records = user.objects.all()
    product_record = product.objects.all()
    if request.method == "POST":
        form = feedbackform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/feedback_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_feedback.html', {'form': form, 'user': user_records, 'product': product_record})


def insert_ContactUs(request):
    if request.method == "POST":
        form = contactusform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/contactus_table')
            except:
                print("---------------", sys.exc_info())
    else:
        form = categoryform()

    return render(request, 'insert_contactus.html', {'form': form})


# ---------------------------------Update Data---------------------------------------
def select_category(request, id):
    cat = category.objects.get(category_id=id)
    return render(request, 'update_category.html', {'category': cat})


def update_Category(request, id):
    cat = category.objects.get(category_id=id)
    form = categoryform(request.POST, instance=cat)
    if form.is_valid():
        form.save()
        return redirect("/category_table")
    return render(request, 'update_category.html', {'category': cat})


def select_subcategory(request, id):
    subcat = subcategory.objects.get(subcategory_id=id)
    subat_records = category.objects.all()
    return render(request, 'update_subcategory.html', {'subcategory': subcat, 'category': subat_records})


def update_Subcategory(request, id):
    subat_records = category.objects.all()
    subcat = subcategory.objects.get(subcategory_id=id)
    form = subcategoryform(request.POST, instance=subcat)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/subcategory_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_subcategory.html', {'subcategory': subcat, 'category': subat_records})


def select_product(request, id):
    prod_records = subcategory.objects.all()
    prod = product.objects.get(product_id=id)
    return render(request, 'update_product.html', {'product': prod, 'subcategory': prod_records})


def update_Product(request, id):
    prod_records = subcategory.objects.all()
    prod = product.objects.get(product_id=id)
    form = productform(request.POST, instance=prod)
    if form.is_valid():
        form.save()
        return redirect("/product_table")
    return render(request, 'update_product.html', {'product': prod, 'subcategory': prod_records})


def select_order(request, id):
    ordr = order.objects.get(order_id=id)
    return render(request, 'update_order.html', {'order': ordr})


def update_Order(request, id):
    ordr = order.objects.get(order_id=id)
    form = orderform(request.POST, instance=ordr)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/order_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_order.html', {'order': ordr})


def select_order_item(request, id):
    ordritem = orderitem.objects.get(order_item_id=id)
    return render(request, 'update_order_item.html', {'ordritem': ordritem})


def update_Order_Item(request, id):
    ordritem = orderitem.objects.get(order_item_id=id)
    form = orderitemform(request.POST, instance=ordritem)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/order_item_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_order_item.html', {'ordritem': ordritem})


def select_payment(request, id):
    pymt = payment.objects.get(payment_id=id)
    return render(request, 'update_payment.html', {'payment': pymt})


def update_Payment(request, id):
    pymt = payment.objects.get(payment_id=id)
    form = paymentform(request.POST, instance=pymt)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/payment_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_payment.html', {'payment': pymt})


def select_feedback(request, id):
    fdbk = feedback.objects.get(feedback_id=id)
    return render(request, 'update_feedback.html', {'feedback': fdbk})


def update_Feedback(request, id):
    fdbk = feedback.objects.get(feedback_id=id)
    form = feedbackform(request.POST, instance=fdbk)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/feedback_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_feedback.html', {'feedback': fdbk})


def select_contactus(request, id):
    cntkus = contactus.objects.get(contact_id=id)
    return render(request, 'update_contactus.html', {'contact': cntkus})


def update_Contactus(request, id):
    cntkus = contactus.objects.get(contact_id=id)
    form = contactusform(request.POST, instance=cntkus)
    print("----------------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/contactus_table")
        except:
            print("---------------", sys.exc_info())
    return render(request, 'update_contactus.html', {'contact': cntkus})


# ---------------------------------Login,Logout Forget & Reset Password---------------------------------------
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = user.objects.filter(email=email, password=password, is_admin=1).count()
        print("--------------", email, "---------", password)
        if val == 1:
            data = user.objects.filter(email=email, password=password, is_admin=1)
            for item in data:
                request.session['admin_email'] = item.email
                request.session['admin_password'] = item.password
                request.session['admin_user_id'] = item.user_id
            if request.POST.get("remember"):  # remember :it's a checkbox name.(in html page)
                response = redirect("/dashboard/")
                response.set_cookie('cookie_admin_email', request.POST[
                    "email"])  # cemail is a key     #email : it's a textbox name (in html page)
                response.set_cookie('cookie_admin_password', request.POST[
                    "password"])  # cpass is a key       #password: it's a textbox name(in html page)
                return response
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/login/')
    else:
        if request.COOKIES.get("cookie_admin_email"):
            return render(request, "login.html",
                          {'c_admin_email': request.COOKIES['cookie_admin_email'],
                           'c_admin_password': request.COOKIES[
                               'cookie_admin_password']})  # cookie1 and cookie2 are keys
        else:
            return render(request, "login.html")
        return render(request, "login.html")


def logout(request):
    # session for logout
    try:
        del request.session['admin_email']
        del request.session['admin_password']
        del request.session['admin_user_id']
        return redirect("/login/")
    except:
        pass
        return redirect("/login/")


# Forget
def forget_password(request):
    return render(request, 'forget_password.html')


# Sending OTP
def sendotp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e
    print("-------------", e)

    obj = user.objects.filter(email=e).count()

    if obj == 1:
        val = user.objects.filter(email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'set_password.html')


# Reseting a password
def set_password(request):
    if request.method == "POST":

        T_otp = request.POST['OTP']
        T_pass = request.POST['pass']
        T_cpass = request.POST['rpass']

        if T_pass == T_cpass:
            e = request.session['temail']

            val = user.objects.filter(email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                user.objects.filter(email=e).update(otp_used=1, password=T_pass)
                return redirect("/login/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "set_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/forget_password")


# ---------------------------------Dashboard, Profile---------------------------------------
# Dashboard
def dashboard(request):
    u = user.objects.all().count()
    ordr = order.objects.all()
    o = order.objects.all().count()
    p = product.objects.all().count()
    f = feedback.objects.all().count()
    return render(request, "dashboard.html", {'order': ordr, 'user': u, 'ordr': o, 'product': p, 'feedback':f})


# Edit Profile
def profile(request):
    a_id = request.session['admin_user_id']
    u = user.objects.get(user_id=a_id)
    register_date = u.registered_date
    register = register_date.strftime("%Y-%m-%d")
    print("====", register_date)
    return render(request, "profile.html", {'ca': u, 'register': register})


def update_profile(request):
    a_id = request.session['admin_user_id']
    u = user.objects.get(user_id=a_id)
    form = userform(request.POST, instance=u)
    print("-------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/dashboard/")
        except:
            print("---------------", sys.exc_info())
    else:
        pass
    return render(request, "profile.html", {'ca': u})


# -----------------------------Dashboard-Chart-----------------------------

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard.html")


class ProjectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT product_id_id as id, sum(amount) as amount FROM orderitem i JOIN product p where i.product_id_id = p.product_id GROUP by product_id_id;''')
        qs = cursor.fetchall()

        labels = []
        default_items = []
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


def accept_order(request, id):
    o = order.objects.get(order_id=id)
    o.order_status = 1
    o.save()
    return redirect("/order_table/")


def rejected_order(request, id):
    o = order.objects.get(order_id=id)
    o.order_status = 2
    o.save()
    return redirect("/order_table/")
