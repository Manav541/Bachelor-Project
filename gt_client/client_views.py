import random
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from gt_admin.functions import handle_uploaded_file
from gt_admin.models import user, category, subcategory, product, gallery, order, orderitem, payment, feedback, \
    contactus, cart
from django.shortcuts import render, redirect
from gt_admin.forms import userform, categoryform, subcategoryform, productform, galleryform, orderform, orderitemform, \
    paymentform, feedbackform, contactusform
import sys
from datetime import date

# Create your views here.
# -------------------Home Page------------------
from gt_client.cart import client_Cart


def index(request):
    p = product.objects.all()
    return render(request, "index.html", {'pro': p})


# ---------------------------------Register, Login, Logout ,Forget & Reset Password---------------------------------------

# Registration
def client_register(request):
    if request.method == "POST":
        form = userform(request.POST)
        print("-------------", form.errors)
        print("======", request.POST['is_admin'])
        if form.is_valid():
            try:
                form.save()
                return redirect('/client/client_login')
            except:
                print("---------------", sys.exc_info())
    else:
        form = userform()
    return render(request, 'client_register.html', {'form': form})


# login
def client_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = user.objects.filter(email=email, password=password, is_admin=0).count()
        print("--------------", email, "---------", password)
        if val == 1:
            data = user.objects.filter(email=email, password=password, is_admin=0)
            for item in data:
                request.session['client_email'] = item.email
                request.session['client_password'] = item.password
                request.session['client_user_id'] = item.user_id
            if request.POST.get("remember"):  # remember :it's a checkbox name.(in html page)
                response = redirect("/client/index/")
                response.set_cookie('cookie_client_email', request.POST[
                    "email"])  # cemail is a key     #email : it's a textbox name (in html page)
                response.set_cookie('cookie_client_password', request.POST[
                    "password"])  # cpass is a key       #password: it's a textbox name(in html page)
                return response
            return redirect('/client/index/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/client/client_login/')
    else:
        if request.COOKIES.get("cookie_client_email"):
            return render(request, "client_login.html",
                          {'c_client_email': request.COOKIES['cookie_client_email'],
                           'c_client_password': request.COOKIES[
                               'cookie_client_password']})  # cookie1 and cookie2 are keys
        else:
            return render(request, "client_login.html")
        return render(request, "client_login.html")


# Logout
def client_logout(request):
    # session for logout
    try:
        del request.session['client_email']
        del request.session['client_password']
        del request.session['client_user_id']
        return redirect("/client/client_login/")
    except:
        pass
        return redirect("/client/client_login/")


# Forget
def client_lostpassword(request):
    return render(request, 'client_lost_password.html')


# Sending OTP
def client_sendotp(request):
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
        return render(request, 'client_set_password.html')


# set password
def client_setpassword(request):
    if request.method == "POST":

        T_otp = request.POST['OTP']
        T_pass = request.POST['pass']
        T_cpass = request.POST['rpass']

        if T_pass == T_cpass:
            e = request.session['temail']

            val = user.objects.filter(email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                user.objects.filter(email=e).update(otp_used=1, password=T_pass)
                return redirect("/client/client_login/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "client_set_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "client_set_password.html")

    else:
        return redirect("/client/lost_password")


# Edit Profile
def client_profile(request):
    a_id = request.session['client_user_id']
    u = user.objects.get(user_id=a_id)
    register_date = u.registered_date
    register = register_date.strftime("%Y-%m-%d")
    print("====", register_date)
    o = order.objects.filter(user_id=a_id)
    return render(request, "client_profile.html", {'ca': u, 'register': register, 'order': o})


# Update Profile
def client_updateprofile(request):
    a_id = request.session['client_user_id']
    u = user.objects.get(user_id=a_id)
    form = userform(request.POST, instance=u)
    print("-------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/client/index/")
        except:
            print("---------------", sys.exc_info())
    else:
        pass
    return render(request, "client_profile.html", {'ca': u})


# -------------------------------Contactus Page---------------------------
def client_contactus(request):
    if request.method == "POST":
        form = contactusform(request.POST)
        print("-------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                print("-------------------------", form.errors)
                return redirect('/client/index/')
            except:
                print("--------------jjj", sys.exc_info())
    else:
        form = contactusform()

    return render(request, 'client_contact.html', {'form': form})


# -----------------------------Load Menu-------------------------
def load_menu(request):
    c = category.objects.all()
    s = subcategory.objects.all()
    return render(request, "test.html", {"cat": c, "sub": s})


# -------------------------Shop, Shop details, feedback---------------------
# Product
def client_shop(request):
    prod = product.objects.all()
    page = request.GET.get('page', 1)

    print("page ----------------", page)
    paginator = Paginator(prod, 8)

    try:
        pro = paginator.page(page)
    except PageNotAnInteger:
        pro = paginator.page(1)
    except EmptyPage:
        pro = paginator.page(paginator.num_pages)
    return render(request, "client_shop.html", {'pro': pro})


# Product Details
def client_shopdetails(request, id):
    pro = product.objects.get(product_id=id)
    feed = feedback.objects.filter(product_id=id)  # Showing Feedbacks
    feed_count = feedback.objects.filter(product_id=id).count()
    rate = 0
    for data in feed:
        rate += data.rating

    if feed_count > 0:
        count_rate = rate / feed_count
    else:
        count_rate = None
    return render(request, "client_shopdetails.html",
                  {'pro': pro, 'feed': feed, 'f_count': feed_count, 'count_rate': count_rate})


# Inserting Feebacks
def client_feedback(request):
    if request.method == "POST":
        try:
            description = request.POST['feedback_desc']
            product_id = request.POST['product_id']
            user_id = request.session['client_user_id']
            fdate = date.today()
            rate = request.POST['rating']

            feed = feedback(user_id_id=user_id, product_id_id=product_id, feedback_desc=description,
                            feedback_date=fdate, rating=rate)
            feed.save()
            return redirect("/client/client_shopdetails/%s" % product_id)
        except:
            print("=======", sys.exc_info())
    else:
        pass
    return render(request, "client_shopdetails.html")


# ------------------------Cart-------------------------
# Show Cart+
def client_cart(request):
    if 'client_user_id' in request.session:
        u_id = request.session['client_user_id']
        emp = cart.objects.filter(user_id=u_id)
        sum = 0
        for val in emp:
            sum = sum + (val.product_id.product_price * val.cart_qty)
        return render(request, "client_cart.html", {'cart': emp, 'total': sum})
    else:
        z = cart.objects.all()
        ct = client_Cart(request)
        total = ct.get_total_price()
        return render(request, "client_cart.html", {"cart": z, 'total': total})


# Insert Cart, Update Cart
def insert_cart(request, id):
    if request.method == "POST":
        if 'client_user_id' in request.session:
            u_id = request.session['client_user_id']
            c = cart.objects.filter(product_id_id=id, user_id_id=u_id).count()
            print("======", c)
            if c == 1:
                try:
                    c1 = cart.objects.get(product_id_id=id, user_id_id=u_id)
                    qty = request.POST["cart_qty"]
                    c1.cart_qty = c1.cart_qty + int(qty)
                    c1.total_amt = int(c1.cart_qty) * int(c1.product_id.product_price)
                    c1.save()
                    return redirect('/client/show_cart/')
                except:
                    print("----", sys.exc_info())
            else:
                try:
                    prd_id = id
                    u = request.session["client_user_id"]
                    pro = product.objects.get(product_id=id)
                    qty = int(request.POST.get("cart_qty"))
                    p = pro.product_price
                    d = date.today().strftime("%Y-%m-%d")
                    total_amt = int(p) * int(qty)
                    C = cart(user_id_id=u, product_id_id=prd_id, cart_date=d, cart_qty=qty, total_amt=total_amt)
                    C.save()
                    return redirect('/client/show_cart/')
                except:
                    print("-------", sys.exc_info())
        else:
            try:
                qty = request.POST['cart_qty']
                ct = client_Cart(request)
                pdt = product.objects.get(product_id=id)
                ct.add(product=pdt, quantity=int(qty))
                print(cart)
                return redirect('/client/show_cart/')
            except:
                print("-------", sys.exc_info())

    return render(request, 'client_shopdetails.html')


# Clear cart
def clear_cart(request):
    if 'client_user_id' in request.session:
        u = request.session["client_user_id"]
        c = cart.objects.filter(user_id=u)
        c.delete()
        return redirect('/client/show_cart/')
    else:
        ct = client_Cart(request)
        ct.clear()
        return redirect("/client/show_cart/")


# Update Cart
def update_quantity(request, id):
    qty = request.GET.get('qty')
    val = cart.objects.get(cart_id=id)
    new_qty = int(qty)
    total = new_qty * val.product_id.product_price
    val = cart.objects.filter(cart_id=id).update(cart_qty=new_qty, total_amt=total)
    val.save()


# Delete cart
def destroy_cart(request, id):
    if 'client_user_id' in request.session:
        ct = cart.objects.get(cart_id=id)
        ct.delete()
        return redirect("/client/show_cart/")
    else:
        ct = client_Cart(request)
        p = product.objects.get(product_id=id)
        ct.remove(p)
        return redirect("/client/show_cart/")


def checkout(request):
    u = request.session['client_user_id']
    c = user.objects.get(user_id=u)
    ca = cart.objects.filter(user_id_id=u)
    sum = 0
    for val in ca:
        sum = sum + (val.product_id.product_price * val.cart_qty)
    print("----------", sum)
    shipping = sum + 50
    return render(request, "client_checkout.html", {"user": c, "total": sum, "product": ca})


# Place Order
def place_order(request, total):
    if 'client_user_id' in request.session:
        pay = request.POST['payment_status']
        address = request.POST['address']
        contact = request.POST['contact']
        print("---------- pay -----------", pay)
        amt = total
        print(amt)
        uid = request.session['client_user_id']
        date1 = date.today().strftime("%Y-%m-%d")
        o = order(user_id_id=uid, total_amount=int(amt), order_date=date1, payment_status=pay, order_status=0,
                  address=address, contact=contact)
        o.save()
        id = order.objects.latest('order_id')
        print("--------------------order id--", id)
        c = cart.objects.filter(user_id_id=uid)

        for data in c:
            pid = data.product_id_id
            qty = data.cart_qty
            print("||||||||||||", qty)
            pri = data.product_id.product_price
            total = int(qty) * pri
            print("0000000000000000000000000000000000", total)
        print("||||||||||||||||||", qty)
        o = orderitem(order_quantity=int(qty), product_id_id=pid, order_id_id=id.order_id, amount=total)
        o.save()

        c_delete = cart.objects.filter(user_id_id=uid)
        c_delete.delete()
        return redirect("/client/allorders/")

    return render(request, "client_checkout.html")


def client_allorders(request):
    u_id = request.session['client_user_id']
    o = order.objects.filter(user_id_id=u_id)
    return render(request, "client_order.html", {'order': o, 'total': sum})


# --------------------------------Search------------------------------
def autosuggest(request):
    if 'term' in request.GET:
        qs = product.objects.filter(product_name__istartswith=request.GET.get('term'))
        names = list()
        for x in qs:
            names.append(x.product_name)
        return JsonResponse(names, safe=False)
    return render(request, "client_header.html")


def search(request):
    if request.method == "POST":
        name = request.POST["product_name"]
        pro = product.objects.filter(product_name=name)
    else:
        pro = product.objects.all()
    return render(request, "client_shop.html", {"pro": pro})
