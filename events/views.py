from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Profile, StudentEventRegistration
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    return render(request, "events/home.html")

def events(request):
    events = Event.objects.all()
    return render(request, "events/event_list.html", {'events':events})




def dashboard(request):
    profile_id = request.session.get("profile_id")

    if not profile_id:
        return redirect("login_profile")

    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return redirect("login_profile")

    # Default context
    context = {
        "profile": profile,
        "events": [],          # default empty
        "registrations": []    # default empty
    }

    if profile.profile_role == "Teacher":
        context["events"] = profile.created_events.all()

    elif profile.profile_role == "Student":
        context["registrations"] = StudentEventRegistration.objects.filter(
            email=profile.profile_email
        )

    return render(request, "events/dashboard.html", context)



def register_event(request):
    return render(request, "events/home.html")

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, "events/event_detail.html", {"event": event})


def register_profile(request):
    if request.method == 'POST':
        name = request.POST.get("profile_name")
        email = request.POST.get("profile_email")
        password = request.POST.get("profile_password")
        role = request.POST.get("profile_role")

        # Check uniqueness of profile_name
        if Profile.objects.filter(profile_name=name).exists():
            messages.error(request, "This profile name is already taken. Please choose another one.")
            return render(request, "events/register.html", {
                "profile_name": name,
                "profile_email": email,
                "profile_role": role,
            })

        # Create Profile if unique
        Profile.objects.create(
            profile_name=name,
            profile_email=email,
            profile_password=password,
            profile_role=role
        )
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('home')

    return render(request, "events/register.html")



def login_profile(request):
    if request.method == "POST":
        name = request.POST.get("profile_name")
        password = request.POST.get("profile_password")

        try:
            # check if profile exists with given credentials
            profile = Profile.objects.get(profile_name=name, profile_password=password)

            # ✅ Store profile id in session
            request.session["profile_id"] = profile.id
            request.session["profile_name"] = profile.profile_name
            request.session["profile_role"] = profile.profile_role

            messages.success(request, f"Welcome back, {profile.profile_name}!")
            return redirect("dashboard")   # redirect to dashboard directly
        except Profile.DoesNotExist:
            messages.error(request, "Invalid name or password. Please try again.")
            return render(request, "events/login.html")

    return render(request, "events/login.html")


def login(request):
    return render(request, "events/home.html")

def logout(request):
    return render(request, "events/home.html")


def student_event_register(request, event_id):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        course = request.POST.get("course")
        year = request.POST.get("year")
        participant_event = get_object_or_404(Event, pk=event_id)

        StudentEventRegistration.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            course=course,
            year=year,
            event=participant_event
            
        )
        return render(request, "events/success_page.html", {"full_name": full_name, "email": email, "event": participant_event })  # create a success page later

    return render(request, "events/participant_registeration.html")


def success_page(request, full_name, email):
    return render(request, "events/success_page.html", {"full_name" : full_name, "email": email} )


def create_event(request):
    profile_id = request.session.get("profile_id")
    if not profile_id:
        return redirect("login_profile")

    profile = Profile.objects.get(id=profile_id)


    if request.method=="POST":
       event_name=request.POST.get("event_name")
       event_desc=request.POST.get("event_desc")
       event_start_date=request.POST.get("event_start_date")
       event_end_date=request.POST.get("event_end_date")
       event_location=request.POST.get("event_location")

       Event.objects.create(
          event_name=event_name,
          event_desc=event_desc,
          event_start_date=event_start_date,
          event_end_date=event_end_date,
          event_location=event_location, teacher=profile
       )
       return render(request, "events/event_created_success.html")
    return render(request, "events/create_event.html")


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # fetch event or 404

    if request.method == "POST":
        # Get values manually from POST request
        event.event_name = request.POST.get("event_name")
        event.event_start_date = request.POST.get("event_start_date")
        event.event_desc = request.POST.get("event_desc")
        event.event_end_date = request.POST.get("event_end_date")
        event.event_location = request.POST.get("event_location")

        event.save()  # save updated event
        return redirect("event_detail", event_id=event.id)  # redirect to details page after update

    # Render template with pre-filled event data
    return render(request, "events/edit_event.html", {"event": event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect("events")  # redirect to event list after delete

    return render(request, "events/delete_event.html", {"event": event})



def event_participants(request, event_id):
    # Get the event by ID
    event = get_object_or_404(Event, id=event_id)

    # Fetch participants registered for this event
    participants = StudentEventRegistration.objects.filter(event=event)

    context = {
        "event": event,
        "participants": participants,
    }
    return render(request, "events/event_participants.html", context)




def about_creators(request):
    return render(request, "events/about_creators.html")
