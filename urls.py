from django.conf import settings
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MysetPasswordConfirmForm

urlpatterns = [
    path('', views.ProductView.as_view()),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    
    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('topwear/', views.topwear, name='topwear'),
    
    path('banner/', views.banner, name='banner'),
    path('banner/<slug:data>', views.banner, name='bannerdata'),
    
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class = MyPasswordChangeForm, success_url='/passwordchangedone/'), name = 'passwordchange'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passchangedone.html'), name='passwordchangedone'),
    path('checkout/', views.checkout1, name='checkout'),
    
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class= MyPasswordResetForm ), name='password_reset'),
   
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html', form_class= MysetPasswordConfirmForm), name='password_reset_confirm'),
    
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html',), name='password_reset_complete'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
