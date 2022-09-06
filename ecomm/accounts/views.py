# from unicodedata import category
from ast import Or, Sub
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.forms import ColorVariantForm, CouponForm, OrderForm, ProductForm, ProductImageForm, ReviewForm, CatogaryForm, ProfileForm, SizeVariantForm, SubcatogaryForm, ProductUpdateForm, TagForm    #, UserDetailsForm
from accounts.models import Profile, UserDetails, cartItems, cart, Order, OrderItems
from products.models import Coupon, Product, ProductImages, SizeVariant, Catogary, SubCategory, Tag, ProductReview
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
# from django.forms import inlineformset_factory
from django.conf import settings
import random
import uuid
from base.emails import send_forget_password_mail
# Create your views here.


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Account is not verified')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('index')

        messages.warning(request, "Invalid credential")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'account/login.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, 'Email is already exist')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "An confirmation mail was send into your Email, please check it!")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'account/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('index')
    
    except Exception as e:
        return HttpResponse('Invalid Email token')


@login_required
def edit_profile(request, id):
    profile = User.objects.get(id=id)
    # userdetails = UserDetails.objects.get(user_id=id)
    form = ProfileForm(instance=profile)
    # userform = UserDetailsForm(instance=userdetails)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        # userform = UserDetailsForm(request.POST, instance=userdetails)
        if form.is_valid(): # and userform.is_valid():
            form.save() 
            # userform.save()

            messages.success(request, 'Successfully Edit your Profile')
            return redirect('edit_profile/<id>')
        else:
            messages.warning(request, 'Profile is not Edited, Try Again!')
            return redirect('edit_profile/<id>')

    context = {'form': form} #'userform': userform}
    return render(request, 'account/edit_profile.html', context)


def logout_page(request):
    logout(request)
    return redirect('index')


def search(request):
    searched = request.POST['search']
    context = {'products': Product.objects.filter(product_name__icontains=searched)}
    return render(request, 'home/search.html', context)


def catogary(request):
    context = {'catogaries': Catogary.objects.all()}
    return render(request, 'product/catogary.html', context)


def add_catogary(request):
    if request.method == 'POST':
        form = CatogaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Catogary Added Successfully')
            return redirect('add_catogary')
        else:
            messages.warning(request, 'Catogary is not added, Try Again!')
            return redirect('add_catogry')
    else:
        form = CatogaryForm()
        return render(request, 'product/add_catogary.html', {'form': form})


def delete_catogary(request, uid):
    try:
        catogary = Catogary.objects.get(uid=uid)
        catogary.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_Subcategory(request):
    if request.method == 'POST':
        form = SubcatogaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Subcatogary Added Successfully')
            return redirect('add_Subcategory')
        else:
            messages.warning(request, 'Subcatogary is not added, Try Again!')
            return redirect('add_Subcategory')
    form = SubcatogaryForm()
    context = {'form': form}
    return render(request, 'product/add_Subcategory.html', context)


def sub_list(request, slug):
    if(Catogary.objects.filter(slug=slug)):
        subcategory = SubCategory.objects.filter(catogary__slug=slug)
        category = Catogary.objects.filter(slug=slug).first()
        context = {'subcategory':subcategory, 'category': category}
        return render(request, 'product/cat_pro_list.html', context)
    else:
        messages.warning(request, 'Category has not found')
        return redirect('catogary')


def pro_list(request, slug):
    if(SubCategory.objects.filter(slug=slug)):
        product = Product.objects.filter(subcategory__slug=slug)
        subcategory = SubCategory.objects.filter(slug=slug).first()

        product_paginator = Paginator(product, 4)
        page_num = request.GET.get('page')
        try:
            page =  product_paginator.get_page(page_num)
        except EmptyPage:
            page = product_paginator.get_page(product_paginator.num_pages)
        except:
            page = product_paginator.get_page(4)

        context = {'product': product, 'subcategory':subcategory, 'page': page, 'is_paginated': True, 'paginator': product_paginator}
        return render(request, 'product/product_list.html', context)
    else:
        messages.warning(request, 'Category has not found')
        return redirect('catogary')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        # img_form = ProductImageForm(request.POST, request.FILES, prefix='img_form')
        images = request.FILES.getlist('image')

        print(".................METHOD IS POST.................")
        # print(form.errors)
        if form.is_valid():
            # print(form.errors)
            print('forms are validdddddd')
            f = form.save(commit=False)
            f.save()

            for i in images:
                ProductImages.objects.create(product=f, image=i)

            print(" PRODUCT SAVED ")
            
            messages.success(request, 'Product Added Successfully')
            return redirect('add_product')
        else:
            messages.warning(request, 'Product is not added, Try Again!')
            return redirect('add_product')
    else:
        form = ProductForm()
        img_form = ProductImageForm()
        context = {'form': form, 'img_form': img_form}
        return render(request, 'product/add_product.html', context)


def load_subcategories(request):
    catogary_id = request.GET.get('catogary_id')
    subcategories = SubCategory.objects.filter(catogary_id=catogary_id).all()
    # print(list(subcategories.values('id', 'subcategory')))
    return render(request, 'product/subcategory_dropdown_list.html', {'subcategories': subcategories})
    # return JsonResponse(list(subcategories.values('id', 'subcategory')), safe=False)



def delete_product(request, uid):
    try:
        products = Product.objects.get(uid=uid)
        products.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_product(request, uid):
    product = Product.objects.filter(uid=uid).first()
    product_img = ProductImages.objects.filter(product_id=uid).first()
    form = ProductUpdateForm(instance=product)
    img_form = ProductImageForm(instance=product_img)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        # img_form = ProductImageForm(request.POST, request.FILES, prefix='img_form')
        images = request.FILES.getlist('image')
        print(".................METHOD IS POST.................")
        
        if form.is_valid():
            print('forms are validdddddd')
            f = form.save(commit=False)
            f.save()

            for i in images:
                ProductImages.objects.create(product=f, image=i)

            print(" PRODUCT UPDATED ")
            
            messages.success(request, 'Product Updated Successfully')
            return redirect('add_product')
        else:
            messages.warning(request, 'Product is not updated, Try Again!')
            return redirect('add_product')
    # else:
    #     form = ProductForm()
    # img_form = ProductImageForm()
    context = {'form': form, 'img_form': img_form}
    return render (request, 'product/update_product.html', context)


@login_required
def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid=uid)
    print(uid)
    user = request.user
    Cart, _ = cart.objects.get_or_create(user=user, is_paid=False)
    print('user_id = ',user.id)
    cart_item = cartItems.objects.create(cart=Cart, product=product)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = cartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_list(request):
    cart_obj = None
    try:
        cart_obj = cart.objects.get(is_paid=False, user=request.user)
        print('cart :', cart_obj, '/////////')
    except Exception as e:
        print(e)
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid coupon!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon:
            messages.warning(request, 'Coupon alredy exists!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(request, f'Amount must be greater than {coupon_obj[0].min_amount} !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0]. is_expired:
            messages.warning(request, 'Coupon expired!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Coupon applied!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    context = {'cart': cart_obj}
    return render(request, 'account/cart.html', context)


def remove_coupon(request, cart_id):
    Cart = cart.objects.get(uid=cart_id)
    Cart.coupon = None
    Cart.save()
    
    messages.success(request, 'Coupon removed!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def success(request):
    order_id = request.GET.get('order_id')
    Cart = cart.objects.get(razorpay_order_id=order_id)
    Cart.is_paid = True
    Cart.save()
    return HttpResponse("payment Successfull")


def checkout(request):
    cart_obj = None
    cart_obj = cart.objects.get(is_paid=False, user=request.user)
    
    userdetails = UserDetails.objects.filter(user=request.user).first()

    # if cart_obj:
    #     client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    #     payment = client.order.create({'amount': cart_obj.get_cart_total() * 100, 'currency': 'INR', 'payment_capture': 1})
    #     cart_obj.razorpay_order_id = payment['id']
    #     cart_obj.save()

    #     print("**********")
    #     print(payment)
    #     print("**********")
    
    # payment = None

    context = {'cart_obj': cart_obj, 'userdetails': userdetails}
    return render(request, 'account/checkout.html', context)


@login_required
def placeorder(request):
    if request.method == "POST":

        # currentuser = User.objects.filter(user=request.user).first()
        # if not currentuser.first_name:
        #     currentuser.first_name = request.POST.get('fname')
        #     currentuser.last_name = request.POST.get('lname')
        #     # currentuser.email = request.POST.get('email')
        #     currentuser.save()

        if not UserDetails.objects.filter(user=request.user):
            userdetails = UserDetails()
            userdetails.user = request.user
            userdetails.phone = request.POST.get('phone')
            userdetails.address = request.POST.get('address')
            userdetails.country = request.POST.get('country')
            userdetails.state = request.POST.get('state')
            userdetails.city = request.POST.get('city')
            userdetails.pincode = request.POST.get('pincode')
            userdetails.save()

        order_obj = Order()
        order_obj.user = request.user
        order_obj.first_name = request.POST.get('fname')
        order_obj.last_name = request.POST.get('lname')
        order_obj.email = request.POST.get('email')
        order_obj.phone = request.POST.get('phone')
        order_obj.address = request.POST.get('address')
        order_obj.country = request.POST.get('country')
        order_obj.state = request.POST.get('state')
        order_obj.city = request.POST.get('city')
        order_obj.pincode = request.POST.get('pincode')

        order_obj.payment_mode = request.POST.get('payment_mode')
        order_obj.payment_id = request.POST.get('payment_id')

        Cart = cart.objects.filter(user=request.user)

        total_price = 0
        for item in Cart:
            total_price = item.get_cart_total()

        order_obj.total_price = total_price
        track_no = 'hi'+str(random.randint(11111111,99999999))
        while Order.objects.filter(tracking_no=track_no) is None:
            track_no = 'hi'+str(random.randint(11111111,99999999))

        order_obj.tracking_no = track_no
        print(track_no)
        print(total_price)
        order_obj.save()

        orderitem_obj = cartItems.objects.filter(cart__user=request.user)
        for item in orderitem_obj:
            OrderItems.objects.create(
                order = order_obj,
                product = item.product,
                # coupon = item.cart.coupon,
                price = item.get_product_price(),
                quantity = item.quantity
            )

            #to decrase the product quantity from available stock
            orderproduct = Product.objects.filter(uid=item.product_id).first()
            orderproduct.total_quantity = orderproduct.total_quantity - item.quantity
            orderproduct.save()

        # clear users cart
        cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Your order has been placed successfully')
        payMode = request.POST.get('payment_mode')
        if payMode == 'paid by razorpaay':
            return JsonResponse({'status': "Your order has been placed successfull"})

    return redirect('your_orders')


def proceedtopay(request):
    Cart = cart.objects.filter(user=request.user)
    total_price = 0
    for item in Cart:
        total_price = item.get_cart_total()

    return JsonResponse({
        'total_price': total_price
    })


@login_required
def your_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'home/yourOrder.html', context)


def orderview(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitem = OrderItems.objects.filter(order=order)
    context = {'order': order, 'orderitem': orderitem}
    return render(request, 'home/vieworder.html', context)


def delete_order(request, uid):
    try:
        order = Order.objects.get(uid=uid)
        order.delete()
    except Exception as e:
        print(e)

    messages.warning(request, 'Delete Successfully')
    return redirect('your_orders')


def password_reset(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email):
                messages.warning(request, "This email is not found has registered email")
                return redirect('password_reset')
            
            useremail = User.objects.filter(email=email)
            forget_password_token = str(uuid.uuid4())
            print('//////////',forget_password_token,'//////////')
            send_forget_password_mail(useremail, forget_password_token)
            messages.success(request, "We've mailed the instructions for setting password. Please check your email")
            return HttpResponseRedirect(request.path_info)

            
    except Exception as e:
        print(e)
    
    return render(request, 'account/password_reset_form.html')


def reset_password(request, forget_password_token):
    try:
        profile_obj = Profile.objects.filter(forget_password_token=forget_password_token)

    except Exception as e:
        print(e)
    return render(request, 'account/pass_reset_confirm.html')


def pass_reset_complete(request):
    return render(request, 'account/pass_reset_complete.html')


def dashboard(request):
    return render(request, 'home/dashboard.html')


def add_colorvariant(request):
    if request.method == 'POST':
        form = ColorVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Color Added Successfully')
            return redirect('add_colorvariant')
        else:
            messages.warning(request, 'Color is not added, Try Again!')
            return redirect('add_colorvariant')
    else:
        form = ColorVariantForm()
        return render(request, 'product/add_colorvariant.html', {'form': form})


def add_sizevariant(request):
    if request.method == 'POST':
        form = SizeVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Size Added Successfully')
            return redirect('add_sizevariant')
        else:
            messages.warning(request, 'Size is not added, Try Again!')
            return redirect('add_sizevariant')
    else:
        form = SizeVariantForm()
        return render(request, 'product/add_sizevariant.html', {'form': form})


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Coupon Added Successfully')
            return redirect('add_sizevariant')
        else:
            messages.warning(request, 'Coupon is not added, Try Again!')
            return redirect('add_sizevariant')
    else:
        form = CouponForm()
        return render(request, 'product/add_coupon.html', {'form': form})


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Tag Added Successfully')
            return redirect('add_sizevariant')
        else:
            messages.warning(request, 'Tag is not added, Try Again!')
            return redirect('add_sizevariant')
    else:
        form = TagForm()
        return render(request, 'product/add_tag.html', {'form': form})


def category_adminview(request):
    catogaries = Catogary.objects.all()
    context = {'catogaries': catogaries}
    return render(request, 'product/admin_category.html', context)


def subcategory_adminview(request):
    subcategory = SubCategory.objects.all()
    context = {'subcategory': subcategory}
    return render(request, 'product/admin_subcategory.html', context)


def product_adminview(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product/admin_product.html', context)


def coupon_adminview(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return render(request, 'product/admin_coupon.html', context)


def tag_adminview(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'product/admin_tag.html', context)


def user_adminview(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'product/admin_orderitem.html', context)


def order_adminview(request):
    orders = Order.objects.all()
    orderitems = OrderItems.objects.all()
    context = {'orders': orders, 'orderitems': orderitems}
    return render(request, 'product/admin_order.html', context)


def update_order(request, uid):
    order = Order.objects.get(uid=uid)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()

            messages.success(request, 'Order details updated successfully')
            return redirect('update_order/<uid>')
        else:
            messages.warning(request, 'Product is not updated, Try Again!')
            return redirect('update_order/<uid>')
   
    context = {'form': form}
    return render (request, 'product/update_order.html', context)


def review(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Product.objects.get(uid=product_id)
        review_text = request.POST.get('review_text')
        review_rating = request.POST.get('review_rating')
        user = request.user

        ProductReview(user=user, product=product, review_text=review_text, review_rating=review_rating).save()

        messages.success(request, 'Review Added Successfully')
        return HttpResponseRedirect(request.path_info)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 