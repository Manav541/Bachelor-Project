from django import forms
from gt_admin.models import user, category, subcategory, product, gallery, cart, order, orderitem, payment, feedback, \
    contactus


class userform(forms.ModelForm):
    class Meta:
        model = user
        fields = ["first_name", "last_name", "address", "contact", "email", "password", "registered_date", "is_admin"]


class categoryform(forms.ModelForm):
    class Meta:
        model = category
        fields = ["category_name"]


class subcategoryform(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = ["category_id", "subcategory_name"]


class productform(forms.ModelForm):
    product_image = forms.FileField()

    class Meta:
        model = product
        fields = ["subcategory_id", "product_name", "product_quantity", "product_price", "product_desc",
                  "product_image"]


class galleryform(forms.ModelForm):
    image_path = forms.FileField()

    class Meta:
        model = gallery
        fields = ["product_id", "image_path"]

class cartform(forms.ModelForm):
    class Meta:
        model = cart
        fields = ["product_id","user_id","cart_date","cart_qty","total_amt"]


class orderform(forms.ModelForm):
    class Meta:
        model = order
        fields = ["user_id", "address", "contact", "order_date", "order_status", "total_amount"]


class orderitemform(forms.ModelForm):
    class Meta:
        model = orderitem
        fields = ["product_id", "order_id", "order_quantity", "amount"]


class paymentform(forms.ModelForm):
    class Meta:
        model = payment
        fields = ["order_id", "payment_amount", "payment_status", "payment_date"]


class feedbackform(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ["user_id", "product_id", "feedback_date", "feedback_desc"]


class contactusform(forms.ModelForm):
    class Meta:
        model = contactus
        fields = ["contact_name", "contact_email", "contact_sub", "contact_desc"]
