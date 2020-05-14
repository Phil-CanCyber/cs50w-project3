"""Populate database with data from http://www.pinocchiospizza.net/menu.html"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')

import django
django.setup()


from orders.models import Size, Topping, SubAddon, PizzaName, Pizza, SubName, Sub, Pasta, Salad, DinnerPlatterName, DinnerPlatter

from decimal import Decimal


# ProductSize
SIZES = ("Small", "Large")
for name in SIZES:
    f = Size(name=name)
    f.save()

# Topping
TOPPINGS = (
            "Pepperoni", "Sausage", "Mushrooms", "Onions", "Ham",
            "Canadian Bacon", "Pineapple", "Eggplant", "Tomato & Basil",
            "Green Peppers", "Hamburger", "Spinach", "Artichoke",
            "Buffalo Chicken", "Barbecue Chicken", "Anchovies",
            "Black Olives", "Fresh Garlic", "Zucchini"
)
for name in TOPPINGS:
    f = Topping(name=name)
    f.save()

# SubAddon
SUBADDONS = (
    ("Mushrooms", Decimal("0.50")),
    ("Green Peppers", Decimal("0.50")),
    ("Onions", Decimal("0.50")),
    ("Extra Cheese", Decimal("0.50")),
)
for item in SUBADDONS:
    f = SubAddon(
        name=item[0],
        price=item[1]
    )
    f.save()

# PizzaName
PIZZANAMES = (
    ("Regular", "Qui nisi labore id pariatur ab ad ab magna tamen quis."),
    ("Sicilian", "Si nisi ab fugiat, possumus nulla quibusdam iudicem.")
)
for item in PIZZANAMES:
    f = PizzaName(name=item[0], description=item[1])
    f.save()

# Pizzas
PIZZAS = (
    # Regular Small
    (1, 1, 0, Decimal("12.20")),
    (1, 1, 1, Decimal("13.20")),
    (1, 1, 2, Decimal("14.70")),
    (1, 1, 3, Decimal("15.70")),
    (1, 1, 5, Decimal("17.25")),
    # Regular Large
    (1, 2, 0, Decimal("17.45")),
    (1, 2, 1, Decimal("19.45")),
    (1, 2, 2, Decimal("21.45")),
    (1, 2, 3, Decimal("23.45")),
    (1, 2, 5, Decimal("25.45")),
    # Sicilian Small
    (2, 1, 0, Decimal("23.45")),
    (2, 1, 1, Decimal("25.45")),
    (2, 1, 2, Decimal("27.45")),
    (2, 1, 3, Decimal("28.45")),
    (2, 1, 5, Decimal("29.45")),
    # Sicilian Large
    (2, 2, 0, Decimal("37.70")),
    (2, 2, 1, Decimal("39.70")),
    (2, 2, 2, Decimal("41.70")),
    (2, 2, 3, Decimal("43.70")),
    (2, 2, 5, Decimal("44.70")),
)
for item in PIZZAS:
    f = Pizza(
        name=PizzaName.objects.get(pk=item[0]),
        size=Size.objects.get(pk=item[1]),
        toppings_count=item[2],
        price=item[3]
    )
    f.save()

# SubName
SUBNAMES = (
    ("Cheese", "Cupidatat consectetur an offendit ut admodum eram sed pariatur consectetur."),
    ("Italian", "Quae ubi excepteur ne quem, et ne summis proident."),
    ("Ham + Cheese", "Amet aut occaecat ut sunt aut e fugiat excepteur."),
    ("Meatball", "Fore ut iudicem ubi aute, quamquam a tamen laboris."),
    ("Tuna", "Ea summis fabulas occaecat ad magna commodo praesentibus."),
    ("Turkey", "Quo iis exquisitaque, fore id fabulas ut quorum."),
    ("Chicken Parmigiana", "Commodo ne anim hic in fore nisi hic fabulas."),
    ("Eggplant Parmigiana", "Minim cernantur ullamco, consequat irure tempor nescius nisi."),
    ("Steak", "Et ab despicationes iis cernantur eu tempor."),
    ("Steak + Cheese", "Mandaremus de pariatur nam eu amet magna ut constias."),
    ("Sausage, Peppers & Onions", "Ut export in culpa o fugiat ea appellat."),
    ("Hamburger", "Nam quo sint multos fugiat quo sunt aut ne labore possumus."),
    ("Cheeseburger", "Admodum ipsum aute fabulas quae, si ipsum non quem."),
    ("Fried Chicken", "Est incididunt imitarentur, constias malis possumus."),
    ("Veggie", "Litteris culpa voluptate de quo se voluptatibus."),
)
for item in SUBNAMES:
    f = SubName(
        name=item[0],
        description=item[1]
    )
    f.save()

# Sub
SUBS = (
    (1, 1, Decimal("6.50")),
    (1, 2, Decimal("7.95")),
    (2, 1, Decimal("6.50")),
    (2, 2, Decimal("7.95")),
    (3, 1, Decimal("6.50")),
    (3, 2, Decimal("7.95")),
    (4, 1, Decimal("6.50")),
    (4, 2, Decimal("7.95")),
    (5, 1, Decimal("6.50")),
    (5, 2, Decimal("7.95")),
    (6, 1, Decimal("7.50")),
    (6, 2, Decimal("8.50")),
    (7, 1, Decimal("7.50")),
    (7, 2, Decimal("8.50")),
    (8, 1, Decimal("6.50")),
    (8, 2, Decimal("7.95")),
    (9, 1, Decimal("6.50")),
    (9, 2, Decimal("7.95")),
    (10, 1, Decimal("6.95")),
    (10, 2, Decimal("8.50")),
    (11, 2, Decimal("8.50")),
    (12, 1, Decimal("4.50")),
    (12, 2, Decimal("6.95")),
    (13, 1, Decimal("5.10")),
    (13, 2, Decimal("7.45")),
    (14, 1, Decimal("6.95")),
    (14, 2, Decimal("8.50")),
    (15, 1, Decimal("6.95")),
    (15, 2, Decimal("8.50")),
)
for item in SUBS:
    f = Sub(
        name=SubName.objects.get(pk=item[0]),
        size=Size.objects.get(pk=item[1]),
        price=item[2]
    )
    f.save()

# Pasts
PASTAS = (
    ("Baked Ziti w/Mozzarella", "In nulla arbitror, ut arbitror do ingeniis.", Decimal("6.50")),
    ("Baked Ziti w/Meatballs", "Cupidatat id occaecat ubi duis o appellat se sint.", Decimal("8.75")),
    ("Baked Ziti w/Chicken", "Quibusdam aute legam te enim, non est esse singulis.",  Decimal("9.75"))
)
for item in PASTAS:
    f = Pasta(
        name=item[0],
        description=item[1],
        price=item[2]
    )
    f.save()

# Salad
SALADS = (
    ("Garden Salad", "Quem cernantur hic appellat iis aliquip veniam minim proident tamen.", Decimal("6.25")),
    ("Greek Salad", "Quibusdam imitarentur id mentitum sed illum ab constias est sint.", Decimal("8.25")),
    ("Antipasto", "Arbitror ne aute, fore deserunt pariatur.", Decimal("8.25")),
    ("Salad w/Tuna", "Culpa arbitror ab admodum est est elit velit ea fabulas.", Decimal("8.25")),
)
for item in SALADS:
    f = Salad(
        name=item[0],
        description=item[1],
        price=item[2]
    )
    f.save()

# DinnerPlatterName
DINNERPLATTERNAMES = (
    ("Garden Salad", "Est litteris reprehenderit, et ut duis constias."),
    ("Greek Salad", "Anim nam singulis, irure id voluptate se tamen."),
    ("Antipasto", "Anim qui voluptate ut fugiat, eu quo tractavissent."),
    ("Baked Ziti", "Si aute a labore, vidisse do occaecat."),
    ("Meatball Parm", "Labore quamquam id firmissimum, sed tamen exquisitaque."),
    ("Chicken Parm", "O cillum est nulla ad ne admodum an expetendis."),
)
for item in DINNERPLATTERNAMES:
    f = DinnerPlatterName(
        name=item[0],
        description=item[1]
    )
    f.save()

# DinnerPlatter
DINNERPLATTERS = (
    (1, 1, Decimal("35.00")),
    (1, 2, Decimal("60.00")),
    (2, 1, Decimal("45.00")),
    (2, 2, Decimal("70.00")),
    (3, 1, Decimal("45.00")),
    (3, 2, Decimal("70.00")),
    (4, 1, Decimal("35.00")),
    (4, 2, Decimal("60.00")),
    (5, 1, Decimal("45.00")),
    (5, 2, Decimal("70.00")),
    (6, 1, Decimal("45.00")),
    (6, 2, Decimal("80.00")),
)
for item in DINNERPLATTERS:
    f = DinnerPlatter(
        name=DinnerPlatterName.objects.get(pk=item[0]),
        size=Size.objects.get(pk=item[1]),
        price=item[2]
    )
    f.save()
