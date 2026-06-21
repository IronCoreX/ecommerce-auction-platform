from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    #Auth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #Listings
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),

    #Bids
    path("bid/<int:listing_id>", views.place_bid, name="place_bid"),

    #Watchlist
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),

    #Categories
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category")
]
