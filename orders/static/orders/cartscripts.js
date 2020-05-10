// get CSRF for ajax
function getCookie(name) {
    console.log("getCookie called");
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
console.log("got token:");
console.log(csrftoken);

// get and compile template
var source = document.getElementById("item-template").innerHTML;
var template = Handlebars.compile(source);


// on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log("dom loaded");
    
    // get username
    const userspan = document.getElementById('usernamespan');
    const username = userspan.dataset.username;
    console.log("username:");
    console.log(username);

    // get info from localstorage or initialize
    var cart = JSON.parse(localStorage.getItem(username));
    if (!cart) {
        cart = {
            'count': 0,
            'items': {},
        }
    }

    // update number by cart in navbar
    if(cart.count) {
        updateCartCount(cart.count);
    }
    console.log("cart:");
    console.log(cart);
     
    // build page
    populate_cart(cart, username);

    // add listeners for back to menu and confirm/order buttons
    const back_button = document.getElementById("back_to_menu")
    back_button.addEventListener("click", function (event) {
        localStorage.setItem(username, JSON.stringify(cart));
        window.location.href = "menu";
    });
    const confirm_button = document.getElementById("confirm_order")
    confirm_button.addEventListener("click", function (event) {
        const msg_promise = confirmOrder(cart, username);
        msg_promise.then(msg => {
            var content = document.getElementsByClassName("content")
            content[0].innerHTML = msg;

        });
    });
});


function getMenuItem(itemid) {
    // sends server menu item id and gets info for display
    console.log("getMenuItem called with id:");
    console.log(itemid)
    return new Promise(function (resolve, reject) {
        const request = new XMLHttpRequest();
        request.open('POST', '/getmenuitem');
        request.setRequestHeader('X-CSRFToken', csrftoken)
        // callback for when request complete
        request.onload = () => {
            // extract json
            const jdata = request.responseText
            console.log("response from server:")
            console.log(jdata);
            // return result
            resolve(JSON.parse(jdata))
        }
        //send request
        request.send(itemid);
    })
}


function updateCartCount(count) {
    // updates number by cart in navbar
    console.log("updateCartCount called")
    document.getElementById("cart_count").innerHTML = "(" + count.toString() + ")"
}


function populate_cart(cart, username) {
    // displays all cart items and sets up delete functionality
    console.log("populate_cart called")
    var total = 0;
    if (!cart.count) {
        document.getElementById("total_field").innerHTML = "0.00";
    }
    for (let i = 1; i <= cart.count; i++) {
        var div = document.createElement('div');
        div.id = i.toString();
        document.getElementById('cart_items').appendChild(div);
    }
    for (let i = 1; i <= cart.count; i++) {
        console.log("i: %i", i);
        console.log("item:");
        console.log(cart.items[i.toString()]);
        let id = cart.items[i.toString()].id;
        const menu_item_promise = getMenuItem(id);
        menu_item_promise.then(item => {
            var options = cart.items[i.toString()].options;
            if (!options) {
                options = null;
            }
            var htmlblock = template({
                item_num: i,
                category: item.category,
                name: item.name,
                size: item.size,
                options: options,
                price: (item.price / 100).toFixed(2),
            });
            var div = document.getElementById(i.toString())
            div.innerHTML = htmlblock;
            // ad delete functionality
            var delbutton = div.querySelector('.deleteitem')
            console.log("got button?:")
            console.log(delbutton)
            delbutton.addEventListener("click", function (event) {
                console.log("delete item clicked")
                let num = parseInt(delbutton.dataset.item_id);
                console.log("got num:")
                console.log(num)
                // if not last, renumber items
                if (num < cart.count) {
                    for (let i = num; i < cart.count; i++) {
                        let j = i + 1;
                        console.log("cart.items[i]:")
                        console.log(cart.items[i])
                        console.log("cart.items[j.toString()]:")
                        console.log(cart.items[j.toString()])
                        cart.items[i.toString()] = cart.items[j.toString()];
                    }
                }
                console.log("cart after renumbering:")
                console.log(cart)
                // delete last
                delete cart.items[cart.count.toString()];
                console.log("cart after deleting last:")
                console.log(cart)

                cart.count -= 1;
                // refresh cart
                var myNode = document.getElementById("cart_items");
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.firstChild);
                }
                updateCartCount(cart.count);
                populate_cart(cart, username)
            })
            // count up total price and display at bottom
            total += item.price;
            console.log("running total:")
            console.log(total)
            total_str = (total / 100).toFixed(2).toString()
            document.getElementById("total_field").innerHTML = total_str;
            cart.total = total;
        });
    }
    localStorage.setItem(username, JSON.stringify(cart));
    console.log("end of populate_cart")
}


function confirmOrder(cart, username) {
    // sends order to server
    console.log("confirmOrder called");
    // reset cart in localstorage
    localStorage.removeItem(username);
    console.log("local should be clear, try to get?:");
    console.log(localStorage.getItem(username));
    // clear cart in DOM
    var myNode = document.getElementById("cart_items");
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
    updateCartCount(0);
    // tell server about order
    return new Promise(function (resolve, reject) {
        const request = new XMLHttpRequest();
        request.open('POST', '/cart');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.setRequestHeader('Content-Type', "application/json");
        request.onload = () => {
            // extract json
            const msg = request.responseText
            console.log("response from server:")
            console.log(msg);
            // return result
            resolve(msg)
        }
        request.send(JSON.stringify(cart));
    });
}


function updateTotal(cart, username) {
    // not used?
    // update total when something is deleted
    var total = 0;
    for (let i = 1; i <= cart.count; i++) {
        total += cart.items[i.toString()].price;
    }
    document.getElementById("total_field").innerHTML = (total / 100).toFixed(2);
    cart.total = total;
    localStorage.setItem(username, JSON.stringify(cart));
}