from django.shortcuts import render

# Create your views here.

def road(request):
    context={
        'stages':[1,2,3,4,5,6,7,8],
    }
    return render(request,"roadmap/road.html",context)

def stage(request,id):
    context={
        "courses":[{'num':1,'title':'Django','description':"A django course with lot of bla vla bla vls"},{'num':2,'title':'DP','description':"A django course with lot of bla"},{'num':3,'title':'Greedy','description':"A django course with lot of bla"},{'num':4,'title':'React','description':"A django course with lot of bla"}],
        "id":id
    }
    return render(request,"roadmap/stage.html",context)