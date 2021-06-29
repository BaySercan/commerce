from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages


from .models import Auction, Comment, User, Bid, WatchList, CATEGORIES

class addAuctionForm(forms.Form):
    title = forms.CharField(label="Auction Title", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))
    description = forms.CharField(label="Descriptin", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))
    price = forms.FloatField(label="Price", min_value=1.0, widget=forms.NumberInput(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))
    image = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))
    category = forms.ChoiceField(label="Category", choices=CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}))

class commentForm(forms.Form):
    comment = forms.CharField(label="Your Comment", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'style':'margin-bottom:15px;height:120px'}))

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(duration = True)
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
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
            #return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        print(request.get_full_path)
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
def addAuction(request):
    if request.method == "POST":
        form = addAuctionForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]

            if not image or image == "":
                image = "https://static.umotive.com/img/product_image_thumbnail_placeholder.png"

            auction = Auction()
            auction.title = title
            auction.description = description
            auction.startingPrice = price
            auction.closePrice = price
            auction.lastBid = price
            auction.image = image
            auction.category = category
            auction.duration = True
            auction.user = request.user
            auction.save()
            
            return render(request, "auctions/index.html", {
                "auctions": Auction.objects.filter(duration = True)
            })

        else:
            return render(request, "auctions/addAuction.html", {
                "form": form
            })

    return render(request, "auctions/addAuction.html", {
        "form": addAuctionForm()
    })


def auctionDetails(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    comments = Comment.objects.filter(auction_id=auction_id)
    ctg = ""
    in_watchlist = False
    for c in CATEGORIES:
        if auction.category in c:
            ctg = c[1]

    auction.categoryName = ctg

    wl = WatchList.objects.filter(user_id = request.user.id, auction_id=auction.id)

    if wl:
        in_watchlist = True

    return render(request, "auctions/auctionDetails.html", {
        "auction":auction,
        "comments":comments.reverse(),
        "commentForm": commentForm(),
        "in_watchlist": in_watchlist
    })


@login_required
def addComment(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    form = commentForm(request.POST)

    if form.is_valid():
        newComment = Comment()
        newComment.comment = form.cleaned_data["comment"]
        newComment.auction = auction
        newComment.user = request.user
        newComment.save()
        comments = Comment.objects.filter(auction_id=auction_id)

        return HttpResponseRedirect(reverse("auctionDetails", args=(auction_id,)))
    else:
        comments = Comment.objects.filter(auction_id=auction_id)

        ctg = ""
        in_watchlist = False

        for c in CATEGORIES:
            if auction.category in c:
                ctg = c[1]

        auction.category = ctg

        wl = WatchList.objects.filter(user_id = request.user.id, auction_id=auction.id)

        if wl:
            in_watchlist = True

        return render(request, "auctions/auctionDetails.html", {
            "auction":auction,
            "comments":comments.reverse(),
            "commentForm": form,
            "in_watchlist": in_watchlist
        })


@login_required
def addRmvWatchlist(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    user = request.user
    wl = WatchList.objects.filter(user_id = request.user.id).filter(auction_id=auction.id)

    if wl:
        wl.delete()
    else:
        newWli = WatchList()
        newWli.auction = auction
        newWli.user = user
        newWli.save()

    return HttpResponseRedirect(reverse("auctionDetails", args=(auction_id,)))


@login_required   
def mywatchlist(request):
    user = request.user

    userWL = WatchList.objects.filter(user_id = user.id)

    return render(request, "auctions/mywatchlist.html", {
        "watchlist": userWL
    })


@login_required
def placeBid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    user = request.user
    bid = float(request.POST["bid"])

    if bid and (bid > int(auction.lastBid)):
        newBid = Bid()
        newBid.auction = auction
        newBid.amount = bid
        newBid.user = user
        newBid.win = False
        newBid.save()

        auction.lastBid = bid
        auction.save()

        wl = WatchList.objects.filter(user_id = request.user.id).filter(auction_id=auction.id)

        if wl:
            pass
        else:
            newWli = WatchList()
            newWli.auction = auction
            newWli.user = user
            newWli.save()

        messages.success(request, 'Your bid is placed successfully. Good luck!')
    else:
        messages.warning(request, 'Check your bid amount and try again. Your bid must be at least $1 greater than the price.')

    return HttpResponseRedirect(reverse("auctionDetails", args=(auction_id,)))


@login_required
def closeAuction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bidder = Bid.objects.filter(auction_id = auction_id)

    if not bidder:
        messages.warning(request, 'There is no bidder for this auction. You can^t close but cancel it.')
    else:
        winner = Bid.objects.filter(auction_id = auction_id).get(amount=auction.lastBid)
        if auction.user_id == request.user.id:
            auction.winner = winner.user_id
            auction.closeBid = auction.lastBid
            auction.duration = 0
            auction.save()
            messages.success(request, 'You have successfully closed this auction. The winner is ' + request.user.username)
        else:
            messages.warning(request, 'Something went wrong please try again.')

    return HttpResponseRedirect(reverse("auctionDetails", args=(auction_id,)))

    
@login_required
def cancelAuction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)

    if auction.user_id == request.user.id:
        auction.duration = 0
        auction.save()

        bids = Bid.objects.filter(auction_id=auction_id)
        bids.delete()

        watchlist = WatchList.objects.filter(auction_id=auction_id)
        watchlist.delete()

        comments = Comment.objects.filter(auction_id=auction_id)
        comments.delete()
        messages.success(request, 'You have successfully cancelled this auction.')
    else:
        messages.warning(request, 'Something went wrong please try again.')

    return HttpResponseRedirect(reverse("auctionDetails", args=(auction_id,)))


def categories(request):

    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


def categoryListing(request, category_id):

    categoryAuctions = Auction.objects.filter(duration = 1).filter(category=category_id)

    categoryName = ""

    for ctg in CATEGORIES:
        if int(ctg[0]) == int(category_id):
            categoryName = ctg[1]
    
    if categoryName == "":
        return render(request, "auctions/index.html", {
            "auctions": Auction.objects.filter(duration=True)
        })
    

    return render(request, "auctions/index.html", {
        "auctions":categoryAuctions,
        "category": categoryName,
    })