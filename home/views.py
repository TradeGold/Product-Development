from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect
from home.models import  Product,Category,Today_Special,Featured_product_of_month,New as Recepie,FAQ,Youtube_Link,login_register,review,email_verification,add_to_cart,guestcart,checkout_order,temporary_order_store,VideoComment
from .forms import register,login,formcontact
import datetime
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import uuid
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def index(request):
    context = {}
    p = Product.objects.all()
    context["product"] = p
    try:
        today_special = Today_Special.objects.get(id=1)
        id_tuple = (today_special.product_1_id,today_special.product_2_id,today_special.product_3_id)
        special1 = Product.objects.filter(id__in=id_tuple)
        context["today_special"] = special1
    except:
        context["today_special"] = []

    category = Category.objects.all()
    context["category"] = category
    try:
        product_month = Featured_product_of_month.objects.get(id=1)
        z= Product.objects.get(id=product_month.product_of_month_id)
        context['fp_month']=z
    except:
        context['fp_month'] = []
    context["ylink"] = Youtube_Link.objects.all()
    context["display_review"]= review.objects.all()

    return render(request,"index.html",context)
def about(request):
    return render(request,"about.html")
def recepies(request):
    context = {}
    recepie = Recepie.objects.all()
    context["recepie"] = recepie
    return render(request,"recepie.html",context)
def faq(request):
    qa = FAQ.objects.all()
    return render(request,"faq.html",{"qa":qa})
def check(request):
    subject, from_email, to = 'hello', 'david.sapkota123@gmail.com', 'david.sapkota123@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<table><tr><td>Nmae</td><td>Email</td><td>Address</td></tr>' \
                   '<tr><td>Anjal Sapkota Bahadur</td><td>david.sapkota123@gmail.com</td><td>Duwakot-5</td></tr>' \
                   '<tr><td>Hari Ram</td><td>A@g.com</td><td>duwakot</td></tr></table>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return render(request,"check.html")
def sendemailorder(orderuser):
    userid = login_register.objects.get(id=orderuser)
    checkstatus = checkout_order.objects.filter(userid=userid).first()
    sendmessage = checkout_order.objects.filter(userid=userid)
    message = ""
    send_email_to = [checkstatus.userid.email_address]
    if checkstatus.order_status == "Pending":
        message += "<table style='border: 1px solid black'><tr style='border: 1px solid black'><th style='border: 1px solid black'>Product </th> <th style='border: 1px solid black'>Description </th> <th style='border: 1px solid black'>Cake Description </th> <th style='border: 1px solid black'>Quantity</th> <th style='border: 1px solid black'>Unit Price</th> <th style='border: 1px solid black'>Amount </th></tr>"
        sum = 0
        for cs in sendmessage.iterator():
            message += f"<tr style='border: 1px solid black'> <td style='border: 1px solid black'>{cs.productid.product_name}</td> <td style='border: 1px solid black'>{cs.description}</td> <td style='border: 1px solid black'>{cs.cake_description}</td> <td style='border: 1px solid black'>{str(cs.quantity)}</td> <td style='border: 1px solid black'>{str(cs.productid.product_price)}</td> <td style='border: 1px solid black'>" + str(cs.productid.product_price*cs.quantity) +"</td></tr>"
            sum += cs.productid.product_price*cs.quantity
        message+=f"<tr style='border: 1px solid black'><td colspan='4' style='border: 1px solid black'></td> <td style='border: 1px solid black'>Total</td> <td style='border: 1px solid black'>{str(sum)}</td> </tr></table>"
        message += f"<br>Delivery Address: {checkstatus.deliveryaddress}<br> Delivery Date: {checkstatus.deliverydate}<br> Recipient Phone no.: {checkstatus.phoneno}<br> Order Status: Pending<br> Payemnt Method: {checkstatus.payment_method}"
        subject= 'Opera: Ordered Product Detail'
        send_email_to.append(settings.EMAIL_HOST_USER)
    elif checkstatus.order_status == "Accepted":
        subject="Opera: Order Accepted"
        message = "You order has been accepted and being prepared. We will be keeping you updated about your order. Thank You For Patience!"
        message += f"<br>Delivery Address: {checkstatus.deliveryaddress}<br> Delivery Date: {checkstatus.deliverydate}<br> Recipient Phone no.: {checkstatus.phoneno}<br> Order Status: Accepted<br> Payemnt Method: {checkstatus.payment_method}"
    elif checkstatus.order_status == "On The Way":
        subject = "Opera: Order on The Way"
        message = "Your Order Has Left the bakery and is on the way. Thank You!"
        message += f"<br>Delivery Address: {checkstatus.deliveryaddress}<br> Delivery Date: {checkstatus.deliverydate}<br> Recipient Phone no.: {checkstatus.phoneno}<br> Order Status: On The Way<br> Payemnt Method: {checkstatus.payment_method}"

    elif checkstatus.order_status == "Delivered":
        subject = "Opera: Ordered Delivered"
        message = "Thank You For Ordering From Opera Cakes And Bakes. Please remember us for another time. Enjoy!"
        checkout_order.objects.filter(userid=userid).delete()

    elif checkstatus.order_status == "Cancel Order":
        subject = "Opera: Order Canceled"
        message = "Sorry, Your order has been canceled"
        checkout_order.objects.filter(userid=userid).delete()
    else:
        subject = "Opera: Sorry Some Error Occured"
        message = "Cannot identify Order"
        checkout_order.objects.filter(userid=userid).delete()

    from_email, to = settings.EMAIL_HOST_USER, send_email_to
    text_content= "Thank You For Remembering Opera Cakes and Bakes"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(message, "text/html")
    msg.send()

def manageemailfromadmin(id,choice):
    updateorder = checkout_order.objects.filter(userid_id=id).update(order_status=choice)
    sendemailorder(id)
def checkouradditionalinformation(request):
    userid = request.POST.get("id")
    ordername = request.POST.get("name")
    orderaddress = request.POST.get("address")
    deliverydate = request.POST.get("date")
    phoneno = request.POST.get("phno")
    if userid:
        temporary_order_store.objects.filter(userid_id=userid).delete()
        temporary_order_store.objects.create(userid_id=userid,username=ordername,deliveryaddress=orderaddress,deliverydate=deliverydate,phoneno=phoneno)

    return JsonResponse({'success':'success'})
def esewapayment(request):
    if request.method == "GET":
        id = request.GET.get("oid")[:1]
        amountpaid = request.GET.get("amt")

        temp =temporary_order_store.objects.filter(userid_id=id).first()
        getaddtocart = add_to_cart.objects.filter(cartuser_id=id)
        paid = f"Paid with E-Sewa ({amountpaid})"
        if getaddtocart:
            for cc in getaddtocart.iterator():
                fillorder = checkout_order.objects.create(userid=cc.cartuser, productid=cc.cartproduct,
                                                          quantity=cc.quantity, description=cc.description,
                                                          cake_description=cc.cake_description, ordername=temp.username,
                                                          deliveryaddress=temp.deliveryaddress, deliverydate=temp.deliverydate,
                                                          phoneno=temp.phoneno,payment_method=paid)
            getaddtocart.delete()
            sendemailorder(id)
            return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('home')


def checkoutadd(request):
    ordername = request.POST.get("name")
    orderaddress = request.POST.get("address")
    deliverydate = request.POST.get("date")
    phoneno = request.POST.get("phno")
    checkcart = add_to_cart.objects.filter(cartuser_id=request.session["id"])
    if checkcart:
        for cc in checkcart.iterator():
            fillorder = checkout_order.objects.create(userid=cc.cartuser,productid=cc.cartproduct,quantity=cc.quantity,description=cc.description,cake_description=cc.cake_description,ordername=ordername,deliveryaddress=orderaddress,deliverydate=deliverydate,phoneno=phoneno)
        checkcart.delete()
        sendemailorder(request.session["id"])
    return JsonResponse({'success':'success'})
@csrf_exempt
def view_add_to_cart(request):
    productid = request.POST.get("pid")
    quantityy = request.POST.get("quantity")
    description = "abc"
    cakename = request.POST.get("cakename")
    size = request.POST.get("size")
    fulldescription = ""

    if cakename or size:
        fulldescription = f"What to write on your cake:{cakename},  Size:  {size}"

    if "id" in request.session:
        user = login_register.objects.get(id=request.session["id"])
        product = Product.objects.get(id=int(productid))
        check_cart = add_to_cart.objects.filter(cartproduct=product,cartuser=user)
        if check_cart:
            check_cart.update(quantity=quantityy,description=description,cake_description=fulldescription)
        else:
            insertcart =add_to_cart.objects.create(cartproduct=product,cartuser=user,quantity=quantityy,description=description,cake_description=fulldescription)
            insertcart.save()

        getcart = len(add_to_cart.objects.filter(cartuser=user))
    elif "guestid" in request.session:
        product = Product.objects.get(id=int(productid))
        check_cart = guestcart.objects.filter(cartproduct=product, guestuser=request.session["guestid"])
        if check_cart:
            check_cart.update(quantity=quantityy, description=description, cake_description=fulldescription)
        else:
            insertcart = guestcart.objects.create(cartproduct=product, guestuser=request.session["guestid"], quantity=quantityy,
                                                    description=description, cake_description=fulldescription)
            insertcart.save()
        getcart = len(guestcart.objects.filter(guestuser=request.session["guestid"]))
    else:
        guestid = uuid.uuid4().hex
        request.session["guestid"]=guestid
        product = Product.objects.get(id=int(productid))
        insertcart = guestcart.objects.create(cartproduct=product, guestuser=request.session["guestid"],
                                              quantity=quantityy,
                                              description=description, cake_description=fulldescription)
        insertcart.save()
        getcart = 1
    return JsonResponse({'status': getcart})
def cartqtyupdate(request):
    qty = request.POST.get("qty")
    productid = request.POST.get("id")
    if "id" in request.session:

        checkcart = add_to_cart.objects.filter(cartuser_id=int(request.session["id"]), cartproduct_id=productid).update(quantity=qty)
        mess = "success"
    elif "guestid" in request.session:
        checkcart = guestcart.objects.filter(guestuser=request.session["guestid"], cartproduct_id=productid).update(quantity=qty)
        mess = "success"
    else:
        mess = "failure"
    return JsonResponse({'status': mess})
def cartremove(request):
    productid = request.POST.get("id")

    if "id" in request.session:
        delcart = add_to_cart.objects.filter(cartuser_id=int(request.session["id"]),cartproduct_id=productid).delete()
        getcart= add_to_cart.objects.filter(cartuser_id=int(request.session["id"]))


    elif "guestid" in request.session:
        delcart = guestcart.objects.filter(guestuser=request.session["guestid"],cartproduct_id=productid).delete()
        getcart = guestcart.objects.filter(guestuser=request.session["guestid"])

    else:
        context = {}
        getcart = ""
    return JsonResponse({'getcart':len(getcart)})

def cart(request):
    context = {}
    if "id" in request.session:

        getuser = login_register.objects.get(id=request.session["id"])
        getcart = add_to_cart.objects.filter(cartuser=getuser)
        context["cartitem"] = getcart
    elif "guestid" in request.session:
        getcart = guestcart.objects.filter(guestuser=request.session["guestid"])
        context["cartitem"] = getcart
    else:
        context = {}
    return render(request,"cart.html",context)
def checkout(request):
    context = {}
    sum = 0
    order_i = ""
    if "id" in request.session:
        context["cartall"] = add_to_cart.objects.filter(cartuser_id=request.session["id"])
        checkpreviousorder = checkout_order.objects.filter(userid=request.session["id"])

    elif "guestid" in request.session:
        context["cartall"] = guestcart.objects.filter(guestuser=request.session["guestid"])
        checkpreviousorder = False

    else:
        context["cartall"] = ""
        checkpreviousorder = True
    for c in context["cartall"]:
        sum += c.cartproduct.product_price
        order_i += str(c.id)

    context["totalcart"] = sum
    if order_i != "":
        context["orderid"] = order_i[:1]

    context["previousorder"]=checkpreviousorder
    context["uniquenumber"] = uuid.uuid4()
    return render(request,"checkout.html",context)
def productdetail(request,pk):
    context = {}
    product = Product.objects.get(id=pk)
    rproduct = Product.objects.filter(product_category = product.product_category_id)[0:4]
    context['product']=product
    context['rproduct'] = rproduct
    comments = VideoComment.objects.filter(productid_id = pk)
    context['comments'] = comments
    return render(request, "productdetail.html",context)

def video_comment_save(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        comment = request.POST.get("comment")
        comment_by_name = request.session['name']
        mydate = datetime.datetime.now()
        short_date = mydate.strftime("%b-%d-%Y")
        product = Product.objects.get(id=int(product_id))
        VideoComment.objects.create(productid=product,comment=comment,comment_date=short_date,comment_by=comment_by_name)
        return HttpResponseRedirect('/productdetail/'+product_id+'/')
    return redirect('home')

def recepiedetail(request,rd):
    context = {}
    recepie = Recepie.objects.get(id=rd)
    context["recepie"] = recepie
    return render(request,"recepiedetails.html",context)
def categorydetail(request,cat):
    context = {}
    products = Product.objects.filter(product_category=cat)

    context['categoryp'] = products
    return render(request,"categorydetail.html",context)

def liveStreamDetail(request,cat):
    context = {}
    products = Product.objects.filter(product_category=cat)

    context['categoryp'] = products
    return render(request,"LiveStreamingDetail.html",context)
def contact(request):
    if request.method == "GET":
        contactform = formcontact()
        return render(request,"contact.html",{'cform':contactform})
    else:
        if request.method == "POST":
            contactform = formcontact(request.POST)
            if contactform.is_valid():
                name = request.POST["name"]
                subject = request.POST["subject"]
                mes = request.POST["description"]
                email = request.POST["email"]
                email_from = settings.EMAIL_HOST_USER
                email_to = settings.EMAIL_HOST_USER
                message = mes + "\n\nYours \n" + name + "\n" + email
                try:
                    send_mail(subject, message, email_from, [email_to],fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return render(request, "contact.html", {'cform': formcontact(),"success":"Message Successfully Sent!"})
            else:
                return render(request, "contact.html", {'cform': contactform})
def logout(request):
    request.session.flush()
    return redirect('home')
def viewsubmitreview(request):
    if request.method == "POST":
        u = request.POST.get("userid")
        reviews = request.POST.get("reviewtext")
        if reviews == "":
            return redirect('home')
        else:
            login_instance = login_register.objects.get(id=int(u))
            savereview = review.objects.create(user=login_instance,review=reviews,reviewdate=datetime.date.today())
            if savereview:
                request.session['review'] = True
            return redirect('home')
    else:
        return redirect(request.build_absolute_uri())
def send_verification(email,token,request):
    email_from = settings.EMAIL_HOST_USER
    email_to = email
    subject = "Opera: Verify"
    message = f"Please click in the link {request.build_absolute_uri('account_verification/')}{token} to verify"
    send_mail(subject,message,email_from,[email_to],fail_silently=False)

def account_verification(request,token):
    verifyy = email_verification.objects.filter(token=token).first()
    if verifyy:
        verifyy.verify = True
        verifyy.save()
        messages.success(request, "Congratulation! Account successfully created",extra_tags="signinsuccess")
    return redirect('login')

class viewlogin(View):
    def get(self,request):
        form1 = login()
        form2 = register()
        return render(request, "login.html", {"form1":form1,"form2": form2})
    @method_decorator(csrf_protect)
    def post(self,reqeust):
        if "sign_up" in reqeust.POST:
            form = register(reqeust.POST)
            form1 = login()
            tokenid = uuid.uuid4()
            if form.is_valid():
                check = form.save()
                save_verificationn = email_verification.objects.create(user=check,token=tokenid)
                send_verification(check.email_address,tokenid,reqeust)
                return render(reqeust,"login.html",{"form1":form1, "form2":form,"success":"Please check your email for verification."})
            else:
                return render(reqeust, "login.html", {"form1":form1,"form2": form})
        else:
            form1 = login(reqeust.POST)
            form = register()
            if form1.is_valid():
                checkuser = login_register.objects.filter(email_address=reqeust.POST.get("email_address"),password = reqeust.POST.get("password"))
                if checkuser:
                    checkauthincated = email_verification.objects.filter(user=checkuser[0]).first()
                    if checkauthincated:
                        # for ca in checkauthincated:
                        if checkauthincated.verify == True:
                            for sess in checkuser.iterator():
                                reqeust.session['id'] = sess.id
                                reqeust.session['name'] = sess.fullname
                                removeguest(reqeust)
                                checkreview = review.objects.filter(user=sess)
                                if len(checkreview)>0:
                                    reqeust.session['review'] = True
                                return redirect("home")
                        else:
                            return render(reqeust, "login.html", {"form1": form1, "form2": form,
                                                                  "lerror": "Please check your email for verification"})
                else:
                    return render(reqeust,"login.html",{"form1":form1,"form2":form,"lerror":"Please enter valid email and password"})
            else:
                return render(reqeust,"login.html",{"form1":form1,"form2":form})
def removeguest(request):
    if "guestid" in request.session:
        guestcart.objects.filter(guestuser=request.session["guestid"]).delete()
        del request.session["guestid"]