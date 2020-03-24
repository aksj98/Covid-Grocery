from django.shortcuts import render
from django.contrib import auth
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
def display(render):
    return render(request,"display.html")
    
def signIn(request):
    return render(request,"signIn.html")
def shoplist(request):
    '''html="<html><head><title>home page</title></head><body> 
    for i in range(x):
        html=html+"<table border ="5"><tr><td rowspan="2">shopname</td><td>description</td></tr>            <tr><td>Location</td></tr>            </table>"

    html=html+"</body></html>"
'''
    return render(request,"shoplist.html")
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
    location=request.POST.get('location')
    description=request.POST.get('description')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message=("Please enter correct details.")
        return render(request,"signUp.html",{"message":message})
    uid=user['localId']
    data={"name":name,"shopname":shopname,"location":location,"description":description,"status":"1"}
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
