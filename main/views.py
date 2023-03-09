from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.models import User

# Create your views here.
def index(request, id):
    if request.user.is_authenticated == False:
        return redirect('/login')
    
    ls = ToDoList.objects.get(id=id)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("save"):
            for item in ls.item_set.all():
                if request.POST.get('c' + str(item.id)) == "clicked":
                    item.delete()
                else:
                    item.save()                    
        elif request.POST.get("newItem"):
            txt = request.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=True)
            else:
                print(txt + " is invalid")
            
    return render(request, "main/list.html", {"ls": ls})

def home(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    
    return render(request, "main/home.html", {})

def create(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(User=request.user,name=n)
            t.save()
            #request.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form": form})

def view(request):
    if request.user.is_authenticated == False:
        return redirect('/login')
    return render(request, "main/view.html", {})

