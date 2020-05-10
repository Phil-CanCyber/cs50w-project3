from django.urls import path

from orders import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("getoptions", views.getoptions, name="getoptions"),
    path("getmenuitem", views.getmenuitem, name="getmenuitem"),
]
