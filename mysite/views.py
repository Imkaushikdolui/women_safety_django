from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login , authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ContactForm
from .models import Account, Contact
from .location import lat, log
from .mail import send_email

def home(request):
    context = {}
    return render(request, "mysite/home.html", context)

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            raw_password = request.POST.get('password1')
            account = authenticate(request,username=username, password=raw_password)
            if account is not None:
                login(request, account)
                messages.success(request, f'Account created for {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try again.')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'mysite/register.html', context)


from django.contrib import messages

def Login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success login")
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not active.')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'mysite/login.html', context)



def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def delete_account(request, username):
    try:
        user = Account.objects.get(username=username)
        user.delete()
        messages.success(
            request, user.username + ", Your account is deleted successfully!"
        )

    except Account.DoesNotExist:
        messages.error(request, "User doesnot exist")

    return redirect("home")

def emergency_contact(request):
    user = request.user
    if user.is_authenticated:
        contacts = Contact.objects.filter(user=user)
        total_contacts = contacts.count()
        context = {
        "contacts": contacts,
        "total_contacts": total_contacts,
        "user": request.user,
        }
        return render(request, "mysite/emergency_contact.html", context)
    return redirect("login")

def createContact(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user = request.user
            new_contact.save()
            messages.success(request, "New contact created successfully!")
            return redirect("emergency_contact")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "mysite/create_contact.html", {'form': form})

def update_contact(request, pk):
    curr_contact = Contact.objects.get(id=pk)
    name = curr_contact.name
    form = ContactForm(
        initial={
            "name": name,
            "email": curr_contact.email,
            "mobile_no": curr_contact.mobile_no,
            "relation": curr_contact.relation,
        }
    )
    if request.method == "POST":
        form = ContactForm(request.POST, instance=curr_contact)
        if form.is_valid():
            form.save()
            messages.success(request, f"{name} updated successfully!!")
            return redirect("emergency_contact")
    context = {"form": form}
    return render(request, "mysite/create_contact.html", context)

def delete_contact(request, pk):
    curr_contact = Contact.objects.get(id=pk)
    name = curr_contact.name
    if request.method == "POST":
        curr_contact.delete()
        messages.error(request, f"{name} deleted successfully!!")
        return redirect("emergency_contact")
    context = {"item": curr_contact}
    return render(request, "mysite/delete_contact.html", context)

def emergency(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    contacts = Contact.objects.filter(user=user)
    total_contacts = contacts.count()
    context = {
        "contacts": contacts,
        "total_contacts": total_contacts,
        "user": request.user
    }
    link = f"http://www.google.com/maps/place/{lat},{log}"
    try:
        for contact in contacts:
            send_email(contact.name, contact.email, link, user.name)
            messages.success(request, f"Email delivered to {contact.name}")
    except:
        messages.error(request, "Something went wrong when sending email")
    return render(request, "mysite/emergency_contact.html", context)


def women_rights(request):
    return render(request, "mysite/women_rights.html", {"title": "women_rights"})

def women_laws(request):
    return render(request, "mysite/women_laws.html", {"title": "women_laws"})

def helpline_numbers(request):
    return render(request, "mysite/helpline_numbers.html", {"title": "helpline_numbers"})

def ngo_details(request):
    return render(request, "mysite/ngo_details.html", {"title": "ngo_details"})

def gallery(request):
    return render(request, "mysite/gallery.html", {"title": "Gallery"})

