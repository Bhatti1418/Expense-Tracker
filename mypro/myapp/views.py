from django.db.models import DecimalField
from django.shortcuts import render, HttpResponse, reverse, redirect
from .models import Items, Balance
from django.contrib.auth.models import User  # Use Django's built-in User model for authentication
from django.contrib.auth import authenticate, login

def mysignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Ensure fields are not empty
        if not username or not password:
            return HttpResponse("All fields are required.", status=400)

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.", status=400)

        # Create a new user
        User.objects.create_user(username=username, password=password)
        return redirect('mylogin')  # Redirect to login page after signup

    return render(request, 'signup.html')


def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('homepage')  # Redirect to homepage
        else:
            return HttpResponse("Invalid credentials. Please try again.", status=401)

    return render(request, 'login.html')


def homepage(request):
    # Retrieve all items from the Items model (if you still want to show them)
    obj_item = Items.objects.all()

    # Get the most recent balance (assuming only one balance record)
    balance = Balance.objects.get(id=5)  # You can use .first() or other methods depending on how many records you have

    return render(request, 'home.html', {'itm': obj_item, 'balance': balance})


def myprofile(request):
    return render(request, 'profile.html')


def mytransaction(request):
    # Fetch all items from the database
    obj_item = Items.objects.all()
    return render(request, 'transaction.html', {'itm': obj_item})


def myadditem(request):
    if request.method == 'POST':
        # Get item details from the form
        it = request.POST['itemName']
        ps = float(request.POST['price'])
        qty = int(request.POST['quantity'])
        tot = ps * qty
        balance = Balance.objects.get(id=5)
        if balance.remaining_balance >= tot:  # Check if there's enough balance
            balance.remaining_balance -= tot
            balance.spend_amount = balance.count + tot
            balance.count = balance.count + tot
            balance.save()
        else:
            # Handle insufficient balance
            return render(request, 'add_item.html', {'error': 'Insufficient balance'})

        # Save the item to the database
        new_item = Items(name=it, price=ps, quantity=qty, total=tot)
        new_item.save()

        # Redirect to the homepage after saving
        return redirect('homepage')  # 'homepage' should match the URL name

    return render(request, 'add_item.html')


def delete(request, id):
    new_item = Items.objects.get(pk=id)
    try:
        new_item.delete()
        return redirect(reverse('homepage'))

    except:
        return HttpResponse('Data not found....')


def update_item(request, id):
    item = Items.objects.get(pk=id)

    if request.method == 'POST':
        it = request.POST.get('itemName')
        ps = float(request.POST.get('price'))
        qty = int(request.POST.get('quantity'))
        tot = ps * qty

        # Check for missing fields
        if not it or not ps or not qty:
            return HttpResponse("All fields are required.", status=400)

        # Update the item
        item.name = it
        item.price = ps
        item.quantity = qty
        item.total = tot

        try:
            item.save()
            return redirect(reverse('homepage'))
        except:
            return HttpResponse('Invalid Data....')

    return render(request, 'updating_form.html', {'obj': item})

def mybalance(request):
    if request.method == 'POST':
        # Get the balance from the form
        bal = request.POST['balance']

        # Save the balance in the 'Balance' model
        new_balance = Balance.objects.get(id=5)
        new_balance.balance = bal
        new_balance.remaining_balance = bal
        new_balance.spend_amount = 0
        new_balance.count = 0
        new_balance.save()

        # Redirect to the homepage after saving
        return redirect('homepage')

    return render(request, 'add_balance.html')

