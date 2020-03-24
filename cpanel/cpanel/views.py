from django.shortcuts import render
from django.contrib import auth
import pyrebase
config={
    'apiKey': "AIzaSyCLjLncnTczSOD7yJd-mgSZLPoLl8icUZw",
    'authDomain': "cpanel-dee36.firebaseapp.com",
    'databaseURL': "https://cpanel-dee36.firebaseio.com",
    'projectId': "cpanel-dee36",
    'storageBucket': "cpanel-dee36.appspot.com",
    'messagingSenderId': "327800301185",
    'appId': "1:327800301185:web:a88b58fd51d71552f80f80",
    'measurementId': "G-S52R4GBPVW"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def signIn(request):
    return render(request,"signIn.html")

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
