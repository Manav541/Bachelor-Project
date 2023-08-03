from django.db import models


# Create your models here.
class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    registered_date = models.DateField(null=True)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)
    is_admin = models.CharField(max_length=10, null=False)

    class Meta:
        db_table = "user"


class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    class Meta:
        db_table = "category"


class contactus(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=30)
    contact_email = models.EmailField(unique=True)
    contact_sub = models.CharField(max_length=100)
    contact_desc = models.CharField(max_length=300)

    class Meta:
        db_table = "contactus"


class subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=20)

    class Meta:
        db_table = "subcategory"


class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    subcategory_id = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150)
    product_quantity = models.IntegerField(null=False)
    product_price = models.IntegerField(null=False)
    product_desc = models.CharField(max_length=300)
    product_image = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "product"


class gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=200)

    class Meta:
        db_table = "gallery"


class cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    cart_date = models.DateField()
    cart_qty = models.IntegerField()
    total_amt = models.IntegerField()

    class Meta:
        db_table = "cart"


class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=10)
    order_date = models.DateField(null=False)
    order_status = models.CharField(max_length=20)
    total_amount = models.IntegerField(null=False)
    payment_status = models.CharField(max_length=20)

    class Meta:
        db_table = "order"


class orderitem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)

    class Meta:
        db_table = "orderitem"


class payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    payment_amount = models.IntegerField(null=False)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateField(null=False)

    class Meta:
        db_table = "payment"


class feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    feedback_date = models.DateField(null=False)
    feedback_desc = models.CharField(max_length=200)
    rating = models.IntegerField()

    class Meta:
        db_table = "feedback"
