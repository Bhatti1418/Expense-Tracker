from django.db.models import DecimalField
from django.shortcuts import render, HttpResponse, reverse, redirect
from .models import Items, Balance, Client
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
    user = request.user

    try:
        # Retrieve the client associated with the user
        client = Client.objects.get(user=user)

        # Try to get the balance for the client
        try:
            balance = Balance.objects.get(client=client)
        except Balance.DoesNotExist:
            # If no balance exists, create a new one
            balance = Balance.objects.create(client=client, balance=0, remaining_balance=0, spend_amount=0, count=0)

        # Retrieve items for the client (if needed)
        items = Items.objects.filter(client=client)

        return render(request, 'home.html', {'itm': items, 'balance': balance})

    except Client.DoesNotExist:
        return HttpResponse("Client not found.", status=404)



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

        # get the current login user
        user = request.user

        try:
            # retrieve the client associated with the login user
            client = Client.objects.get(user=user)

            # get the client balance
            balance = Balance.objects.get(client=client)

            if balance.remaining_balance >= tot:
                # Update the balance
                balance.remaining_balance -= tot
                balance.spend_amount = balance.spend_amount  + tot
                balance.save()
            else:
                return render(request, 'add_item.html', {'error': 'Insufficient balance'})

            # save the item to the database
            new_item = Items(name=it, price=ps, quantity=qty, total=tot, client=client)
            new_item.save()

            # after saving redirect to the homepage
            return redirect('homepage')

        except Client.DoesNotExist:
            return HttpResponse("Client not found.", status=404)

    return render(request, 'add_item.html')


def delete(request, id):
    try:
        new_item = Items.objects.get(pk=id)

        client = new_item.client

        # get the balance for the client
        balance = Balance.objects.get(client=client)

        balance.remaining_balance = balance.remaining_balance + new_item.total
        balance.spend_amount = balance.spend_amount - new_item.total
        balance.save()

        new_item.delete()
        return redirect(reverse('homepage'))
    # if item is not found
    except Items.DoesNotExist:
        return HttpResponse('Item not found')

def update_item(request, id):
    # retrieve the item using its primary key (id)
    item = Items.objects.get(pk=id)
    client = item.client  # Get the client associated with the item

    # retrieve the balance for the client
    balance = Balance.objects.get(client=client)

    if request.method == 'POST':
        # get the updated item details from the form
        it = request.POST.get('itemName')
        ps = float(request.POST.get('price'))
        qty = int(request.POST.get('quantity'))
        new_total = ps * qty  # Calculate the new total

        # check for missing fields
        if not it or not ps or not qty:
            return HttpResponse("All fields are required.")

        # calculate the difference between the old and new totals
        total_difference = new_total - item.total

        # check if there is enough balance for the new total
        if balance.remaining_balance >= total_difference:
            # update the balance
            balance.remaining_balance -= total_difference
            balance.spend_amount += total_difference
            balance.save()
        else:
            # handle insufficient balance
            return HttpResponse("Insufficient balance to update the item.")

        # update the item fields
        item.name = it
        item.price = ps
        item.quantity = qty
        item.total = new_total

        try:
            # save the updated item
            item.save()
            return redirect(reverse('homepage'))
        except:
            return HttpResponse("Invalid Data....")

    # render the update form with the current item details
    return render(request, 'updating_form.html', {'obj': item})


def mybalance(request):
    if request.method == 'POST':
        # get the balance from the form
        bal = request.POST['balance']

        # get the logged-in user
        user = request.user

        try:
            # retrieve the client associated with the user
            client = Client.objects.get(user=user)

            # retrieve or create the balance for the client
            balance, created = Balance.objects.get_or_create(client=client)

            # Update the balance
            balance.balance = bal
            balance.remaining_balance = bal  # assuming remaining balance starts equal to the total balance
            balance.spend_amount = 0  # assuming no spending initially
            balance.count = 0  # assuming the initial count is zero
            balance.save()

            # redirect to the homepage after saving
            return redirect('homepage')

        except Client.DoesNotExist:
            return HttpResponse("Client not found.", status=404)

    return render(request, 'add_balance.html')

def mycatagories(request):
    if request.method == 'POST':
        cat = request.POST['catagory']
        new_item = Items(catagory = cat)
        new_item.save()
        return redirect('homepage')

    return render(request, 'catagories.html')

