from home.models import *
from .forms import review

def add_variable_to_context(request):

    category = Category.objects.all()
    plist = []
    for c in category.iterator():
        product = Product.objects.filter(product_category=c.id)
        plist.append(list(product))

    return {"ddproduct":plist,"ddcategory":category}
def showcart(request):
    context={}
    if "id" in request.session:
        getcart = add_to_cart.objects.filter(cartuser_id=int(request.session["id"]))
        context["cartitemlength"] = len(getcart)
    elif "guestid" in request.session:
        getcart = guestcart.objects.filter(guestuser=request.session["guestid"])
        context["cartitemlength"] = len(getcart)
    else:
        context["cartitemlength"]=0
    return context
