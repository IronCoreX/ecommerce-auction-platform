from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from .models import User, Listings, Comment, Category, Bid


def index(request):
    active_listings = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url")
        category_id = request.POST["category"]

        category = Category.objects.get(id=category_id)

        Listings.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            owner=request.user,
            active=True
        )

        return redirect("index")

    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })

def listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    highest_bid = listing.bids.order_by("-amount").first()

    if highest_bid:
        current_price = highest_bid.amount
    else:
        current_price = listing.starting_bid
    
    # Handle comment submission
    if request.method == "POST":
        comment_text = request.POST.get("comment")

        if comment_text and request.user.is_authenticated:
            Comment.objects.create(
                user=request.user,
                listing=listing,
                text=comment_text
            )
            return redirect("listing", listing_id=listing.id)
    
    # Fetch Comments
    comments = listing.comments.all().order_by("-timestamp")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": comments
    })

def place_bid(request, listing_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
    listing = Listings.objects.get(id=listing_id)
    bid_amount = Decimal(request.POST["bid"])

    highest_bid = listing.bids.order_by("-amount").first()

    if highest_bid:
        current_price = highest_bid.amount
    else:
        current_price = listing.starting_bid
    if bid_amount <= current_price:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your bid must be higher than the current price."
        })

    Bid.objects.create(
        user=request.user,
        listing=listing,
        amount=bid_amount
    )

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def toggle_watchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)

    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required 
def close_listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)

    # Only owner can close
    if request.user != listing.owner:
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
    listing.active = False

    highest_bid = listing.bids.order_by("-amount").first()
    if highest_bid:
        listing.winner = highest_bid.user
    
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listings.objects.filter(category=category, active=True)

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })