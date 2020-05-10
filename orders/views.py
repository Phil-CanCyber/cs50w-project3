"""Routing for orders"""

import logging
import json

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import *


logging.basicConfig(level=logging.DEBUG)


def cart(request):
    """associated with the shopping cart page"""
    if request.method == 'POST':
        # ajax calls post to submit order TODO
        logging.info('cart called post')
        user_cart = json.loads(request.body)
        logging.debug("recieved cart:")
        logging.debug(user_cart)
        this_order = Order.objects.create(
            client_id=request.user.id,
            bill=user_cart["total"]/100,
        )
        for key, item in user_cart["items"].items():
            logging.debug("cart item:")
            logging.debug(item)
            if not item["options"]:
                item["options"] = ""
            m_item = MenuItem.objects.get(pk=int(item["id"]))
            logging.debug("got menu item:")
            logging.debug(m_item)
            o_item = OrderItem.objects.create(
                order=this_order,
                menu_item=m_item,
                options=item["options"],
            )
            logging.debug("created order item:")
            logging.debug(o_item)

        return HttpResponse("Order Placed")
    else:
        # initialize page
        logging.info('cart called get')
        if request.user.is_authenticated:
            context = {
                "user": request.user
            }
            return render(request, "orders/cart.html", context)
        else:
            return render(request, "orders/login.html", {"message": "Log in to see cart"})


def getmenuitem(request):
    """for ajax to get details on a menu item from its id"""
    logging.info('getmenuitem called')
    itemid = request.body.decode('utf-8')
    logging.debug('got id:')
    logging.debug(itemid)
    thismenuitem = MenuItem.objects.get(pk=int(itemid))
    return HttpResponse(thismenuitem.json_obj(), content_type="application/json")


def getoptions(request):
    """for ajax to retrive possible options for a menu item from its id"""
    logging.info('getoptions called')
    itemid = request.body.decode('utf-8')
    logging.debug('got id:')
    logging.debug(itemid)
    thismenuitem = MenuItem.objects.get(pk=int(itemid))
    options = list(
        Option.objects.values_list('name', flat=True).filter(category=thismenuitem.category)
    )
    logging.debug('got options list:')
    logging.debug(options)
    joptions = json.dumps(options)
    return HttpResponse(joptions, content_type="application/json")


def index(request):
    """associated with the index page"""
    logging.info('index called')
    if request.user.is_authenticated:
        logging.info('is authenticated')
        context = {
            "user": request.user
        }
    else:
        logging.info('is not authenticated')
        context = {
            "user": None
        }
    return render(request, "orders/index.html", context)

def login_view(request):
    """associated with the login page"""
    if request.method == 'POST':
        logging.info('login called post')
        try:
            username = request.POST["username"]
        except KeyError:
            return render(request, "orders/login.html", {"message": "Missing username"})
        else:
            try:
                password = request.POST["password"]
            except KeyError:
                return render(request, "orders/login.html", {"message": "Missing password"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials"})
    else:
        logging.info('login called get')
        return render(request, "orders/login.html", {"message": None})

def logout_view(request):
    """log a user out"""
    logging.info('logout called')
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out"})


def menu(request):
    """associated with the menu page"""
    # build menu
    menu_dict = dict()
    logging.info('menu called')
    # get all categories
    categories = MenuItem.objects.values_list('category__name', flat=True).distinct()
    for category in categories:
        menu_dict[category] = dict()
        menu_dict[category]['sizes'] = MenuItem.objects.values_list('size__name', flat=True).distinct().filter(category__name=category)
        # get all items in category
        items = MenuItem.objects.values_list('name', flat=True).distinct().filter(category__name=category)
        for item in items:
            menu_dict[category][item] = dict()
            # get all sizes for item
            sizes = MenuItem.objects.values_list('size__name', flat=True).distinct().filter(category__name=category, name=item)
            for size in sizes:
                menu_dict[category][item][size] = dict()
                for key in ['option_num', 'id']:
                    menu_dict[category][item][size][key] = int(MenuItem.objects.values_list(key, flat=True).get(category__name=category, name=item, size__name=size))
                menu_dict[category][item][size]['price'] = float(MenuItem.objects.values_list('price', flat=True).get(category__name=category, name=item, size__name=size))
    context = {
        'menu_dict': menu_dict,
    }
    return render(request, "orders/menu.html", context)


def register_view(request):
    """associated with the register page"""
    if request.method == 'POST':
        # check they provided all info and collect it
        user_info = dict()
        for key in ['username', 'first_name', 'last_name', "email", "pass1", "pass2"]:
            if not request.POST[key]:
                return render(request, "orders/register.html", {"message": f"Missing {key}"})
            else:
                user_info[key] = request.POST[key]
        # check passwords match
        if user_info["pass1"] != user_info["pass2"]:
            return render(request, "orders/register.html", {"message": "Passwords don't match"})
        # create the new user
        try:
            new_user = User.objects.create_user(
                username=user_info["username"],
                first_name=user_info["first_name"],
                last_name=user_info["last_name"],
                password=user_info["pass1"],
                email=user_info["email"],
                is_staff=False
            )
            new_user.save()
        except:
            return HttpResponseServerError("There was a problem creating the new user")
        # log user in and redirect to index
        user = authenticate(request, username=user_info["username"], password=user_info["pass1"])
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # if coming via GET, serve registration form
    else:
        return render(request, "orders/register.html")
