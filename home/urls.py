from django.contrib import admin
from django.urls import path
from home.views import index,about,cart,liveStreamDetail,checkout,contact,faq,viewlogin,productdetail,recepies,recepiedetail,categorydetail,check,logout,viewsubmitreview,account_verification,view_add_to_cart,cartremove,cartqtyupdate,checkoutadd,esewapayment,checkouradditionalinformation,video_comment_save
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',index,name="home"),
    path('about/',about,name = "about"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('contact/', contact, name="contact"),
    path('faq/', faq, name="faq"),
    path('login/', viewlogin.as_view(), name="login"),

    path(r'productdetail/<int:pk>/', productdetail, name="productdetail"),
    path('recepies/', recepies, name="recepie"),
    path('recepiedetail/<int:rd>/', recepiedetail, name="recepiedetail"),
    path('category/<int:cat>/',categorydetail,name="catdetail"),
    path('logout/',logout,name="logout"),
    path('check/',check,name="check"),
    path('submitreview/',viewsubmitreview,name="submitreview"),
    path('login/account_verification/<slug:token>',account_verification,name='verify'),
    path('addToCart/',view_add_to_cart,name='addtocart'),
    path('removecart/',cartremove,name='removecart'),
    path('cartquantityupdate/',cartqtyupdate,name='cartquantityupdate'),
    path('checkoutorder/',checkoutadd,name='checkoutorder'),
    path('esewapaymentsuccess/',esewapayment,name='esewapayment'),
    path('videocomment/',video_comment_save,name='videocomment'),
    path('addtemporaryorder/',checkouradditionalinformation,name='checkourtemporaryorder'),
    path('live/<int:cat>/',liveStreamDetail,name="live"),





]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)