from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addAuction", views.addAuction, name="addAuction"),
    path("<int:auction_id>", views.auctionDetails, name="auctionDetails"),
    path("<int:auction_id>/addComment", views.addComment, name="addComment"),
    path("<int:auction_id>/addRmvWatchlist", views.addRmvWatchlist, name="addRmvWatchlist"),
    path("mywatchlist", views.mywatchlist, name="mywatchlist"),
    path("categories", views.categories, name="categories"),
    path("<int:category_id>categoryListing", views.categoryListing, name="categoryListing"),
    path("<int:auction_id>/placeBid", views.placeBid, name="placeBid"),
    path("<int:auction_id>/closeAuction", views.closeAuction, name="closeAuction"),
    path("<int:auction_id>/cancelAuction", views.cancelAuction, name="cancelAuction"),
]
