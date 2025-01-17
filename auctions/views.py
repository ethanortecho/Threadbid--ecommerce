from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Bids, User, Listing, ListingImage, Comments, Watchlist
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone


def index(request):
    listings = Listing.objects.all()
    return render(request, 
                  "auctions/index.html",
                    {'listings': listings,
                    "category_choices": Listing.CATEGORY_CHOICES,}
                  )

def add_to_watchlist(request, id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=id)
        Watchlist.objects.get_or_create(user=request.user, listing=listing)
        return redirect('listing', id=id)  # Redirect back to the listing page

@login_required(login_url='login')
def watchlist(request):
    watchlist = Watchlist.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {'watchlist' : watchlist})


def my_listings(request):
    user_listings = Listing.objects.filter(seller=request.user)
    return render(request, "auctions/my_listings.html", {'user_listings': user_listings})

@login_required(login_url='login')
def listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.method == "POST":
        # Check if it's an AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                
                # Handle AJAX bid submissions
                if data.get('form_type') == 'bid':
                    try:
                        bid_amount = float(data.get('bid_amount'))
                        if bid_amount >= listing.minimum_bid():
                            Bids.objects.create(
                                listing=listing,
                                user=request.user,
                                bid=bid_amount
                            )
                            return JsonResponse({
                                'success': True,
                                'new_minimum_bid': listing.minimum_bid(),
                            })
                        else:
                            return JsonResponse({
                                'success': False,
                                'error': 'Bid must be at least the minimum amount'
                            })
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid bid amount'
                        })
                
                # Handle AJAX comment submissions (existing code)
                elif data.get('content'):
                    content = data.get('content')
                    if not content:
                        return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
                        
                    new_comment = Comments.objects.create(
                        listing=listing,
                        user=request.user,
                        content=content
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'comment': {
                            'username': request.user.username,
                            'content': new_comment.content,
                            'created_at': new_comment.created_at.strftime("%B %d, %Y, %I:%M %p")
                        }
                    })

            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        
        # Handle regular form submissions (existing code)
        else:
            form_type = request.POST.get("form_type")
            if form_type == "bid":
                try:
                    bid_amount = float(request.POST["bid_amount"])
                except ValueError:
                    messages.error(request, "Please enter a valid number.")
                    return redirect("listing", id=id)
                
                if bid_amount >= listing.minimum_bid():
                    Bids.objects.create(
                        listing=listing,
                        user=request.user,
                        bid=bid_amount
                    )
            elif form_type == "comment":
                Comments.objects.create(
                    listing=listing,
                    user=request.user,
                    content=request.POST["comment"]
                )

    comments = listing.comments.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        'comments': comments
    })


 

@login_required(login_url='login')
def create_listing(request):
    if request.method=="POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST['category']
        condition = request.POST['condition']
        size = request.POST['size']

        try:
            starting_price = float(request.POST["starting_price"])
        except ValueError:
            return redirect("listing", id=id)
        listing = Listing.objects.create(
            seller = request.user,
            title = title,
            description = description,
            category = category,
            condition = condition,
            starting_price = starting_price,
            size = size
        )

        images = request.FILES.getlist("images")  # Retrieve list of uploaded files
        for image in images:
            ListingImage.objects.create(listing=listing, image=image)



        



    return render(request, 'auctions/create_listing.html', {
        'condition_choices': Listing.CONDITION_CHOICES,
        'category_choices': Listing.CATEGORY_CHOICES,
        'size_choices': Listing.SIZE_CHOICES
    })


def delete_listing(request, id):

    listing = get_object_or_404(Listing, id=id)
    if request.user == listing.seller:
        listing.delete()

    form_type = request.POST['form_type']

    if form_type =='listing':
        return redirect('index')  
    elif form_type == 'my_listing':
        return redirect('my_listings')

def delete_watchlist_item(request, id):

    watchlist_item = get_object_or_404(Watchlist, id=id)
    watchlist_item.delete()

    form_type = request.POST['form_type']

    
    if form_type == 'watchlist':
        return redirect('watchlist')
    
def end_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.user == listing.seller:
        listing.status = False

def search(request):
    query = request.GET.get('query', '').strip()
    category = request.GET.get('category', '').strip()


    if query:
        matching_listings = Listing.objects.filter(title__icontains=query)
    elif category:
        matching_listings = Listing.objects.filter(category__iexact = category)
    else:
        matching_listings = []

    return render(request, "auctions/search_results.html", {
        "matching_listings": matching_listings,
        "query": query,
        "category": category,
        "message": f"Search results for '{query}'" if matching_listings else f"There were no results for '{query}'",
        "category_choices": Listing.CATEGORY_CHOICES,
        "condition_choices": Listing.CONDITION_CHOICES,
        "size_choices": Listing.SIZE_CHOICES
    })


    



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get('content')
            
            if not content:
                return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
                
            listing = get_object_or_404(Listing, id=listing_id)
            new_comment = Comments.objects.create(
                listing=listing,
                user=request.user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'username': request.user.username,
                    'content': new_comment.content,
                    'created_at': new_comment.created_at.strftime("%B %d, %Y, %I:%M %p")
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})