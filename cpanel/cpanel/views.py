from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
import pyrebase
config={
    'apiKey': "AIzaSyDjKBhKFMQXgEsY1Mwu1iF5hciYoDWHXlw",
    'authDomain': "covid-grocer.firebaseapp.com",
    'databaseURL': "https://covid-grocer.firebaseio.com",
    'projectId': "covid-grocer",
    'storageBucket': "covid-grocer.appspot.com",
    'messagingSenderId': "392378464185",
    'appId': "1:392378464185:web:347bde56bd9bd3b49ae868",
    'measurementId': "G-5Z5SR79KCH"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()
def display(request):
    return render(request,"display.html")

def signIn(request):
    return render(request,"signIn.html")
def shoplist(request):
    html="<html><head><title>home page</title></head><body>"
    loc=request.POST.get('loc')
    datab=dict(dict(database.get().val())['users'])

    no_shop_present = True
    for i in datab.keys():
        if datab[i]['details']['location']==loc:
            no_shop_present = False
            html=html+"<table border =\"5\"><tr><td rowspan=\"2\">"+datab[i]['details']["shopname"]+"</td><td>"+datab[i]['details']["description"]+"</td></tr>            <tr><td>"+datab[i]['details']["location"]+"</td></tr>            </table>"


    if no_shop_present:
        html += "<h2>Sorry no shop is registerd for this location on this app</h2>"
    else:
        html+="<br><br><input type=\"button\" value=\"Place Order\" onclick=\"location.href='{% url 'orderdetails' %}'\">"

    html=html+"</body></html>"
    fptr=open("./templates/shoplist.html","w")
    fptr.write(html)
    fptr.close()
    #return HttpResponse(html)
    return render(request,"shoplist.html")

def thankyou(request):
    customer_name = request.POST.get('customername')
    contact = request.POST.get('contact')
    email = request.POST.get('email')
    shop_name = request.POST.get('shopname')
    shop_name = shop_name.replace(" ", "")
    shop_name = shop_name.lower()
    shopping_list = request.POST.get('shoppinglist')

    datab=dict(dict(database.get().val())['users'])

    shop_not_found = True
    for key in datab.keys():
        if datab[key]['details']['shopname'].lower() == shop_name:

            shop_not_found = False
            orderdetails = {"contact": contact, "email": email, "shoppinglist": shopping_list}
            database.child("users").child(key).child("details").child("order_list").child(customer_name).set(orderdetails)

    html="<html><head><title>home page</title></head><body>"
    if shop_not_found:
        html += "<h2>Sorry, Invalid shop name.</h2>"
    else:
        html += "<h2 style=\"text-align: center;\">Thank you for shopping with us. "
    html=html+"</body></html>"

    fptr=open("./templates/thankyou.html","w")
    fptr.write(html)
    fptr.close()

    return render(request, "thankyou.html")

def orderdetails(request):
    return render(request,"order_details.html")
def postsign(request):
    email=request.POST.get('email')
    passw=request.POST.get("pass")
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid email or password"
        return render(request, "signIn.html",{"message":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")

def signUp(request):
    return render(request, "signUp.html")
def postsignUp(request):
    name=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')
    shopname=request.POST.get('shopname')
    shopname = shopname.replace(" ", "")
    shopname = shopname.lower()
    location=request.POST.get('location')
    description=request.POST.get('description')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message=("Please enter correct details.")
        return render(request,"signUp.html",{"message":message})
    uid=user['localId']
    data={"name":name,"shopname":shopname,"location":location,"description":description,"status":"1", "order_list": {"customer name": "grocery list"}}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def Prisoners(request):
    return render(request,"prisoners.html")

def addPrisoner(request):
    return render(request,"addprisoner.html")

def postaddprisoner(request):

    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    prisonerName=request.POST.get('name')
    prisonerID=request.POST.get('id')
    cellNo=request.POST.get('cellno')
    photo=request.POST.get('img1')
    fingerprint=request.POST.get('img2')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    crimedetails=request.POST.get('details')
    arrival=request.POST.get('arrival')
    duration=request.POST.get('duration')

    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    print("info"+str(a))
    data = {
        "prisonerName": prisonerName,
        "prisonerID": prisonerID,
        "cellNo": cellNo,
        "photo": photo,
        "fingerprint": fingerprint,
        "state": state,
        "pincode": pincode,
        "crimedetails": crimedetails,
        "arrival": arrival,
        "duration": duration
    }
    database.child('users').child(a).child('info').child(millis).set(data)
    name=database.child('users').child(a).child('details').child('name').get().val()

    return render(request,"prisoners.html", {'e':name})

def viewPrisoner(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').shallow().get().val()
    lis_time=[]

    for i in timestamps:
        lis_time.append(i)

    lis_time.sort(reverse=True)
    return render(request,"viewprisoner.html")
