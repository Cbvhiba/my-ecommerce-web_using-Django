from django.urls import path
from accounts import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('activate/<email_token>', views.activate_email, name="activate_email"),
    path('edit_profile/<id>', views.edit_profile, name='edit_profile'),
    path('catogary/', views.catogary, name='catogary'),
    path('add_catogary/', views.add_catogary, name='add_catogary'),
    path('add_Subcategory/', views.add_Subcategory, name='add_Subcategory'),
    path('sub_list/<slug>', views.sub_list, name='sub_list'),
    path('pro_list/<slug>', views.pro_list, name='pro_list'),
    path('search/', views.search, name='search'),
    path('delete_catogary/<uid>', views.delete_catogary, name='delete_catogary'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<uid>', views.update_product, name='update_product'),
    path('delete_product/<uid>', views.delete_product, name='delete_product'),
    path('logout/', views.logout_page, name='logout'),
    path('cart/', views.cart_list, name='cart'),
    path('add_to_cart/<uid>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<cart_item_uid>', views.remove_cart, name='remove_cart'),
    path('remove_coupon/<cart_id>', views.remove_coupon, name='remove_coupon'),
    path('success/', views.success, name='success'),
    path('checkout/', views.checkout, name='checkout'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('proceedtopay/', views.proceedtopay, name='proceedtopay'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('your_orders/', views.your_orders, name='your_orders'),
    path('orderview/<t_no>', views.orderview, name='orderview'),
    path('add_colorvariant/', views.add_colorvariant, name='add_colorvariant'),
    path('add_sizevariant/', views.add_sizevariant, name='add_sizevariant'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('add_tag/', views.add_tag, name='add_tag'),

    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'), # AJAX

    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset_password/<forget_password_token>', views.reset_password, name='reset_password'),
    path('pass_reset_complete/', views.pass_reset_complete, name='pass_reset_complete'),
]