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

var activechoice = false;

// on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log("dom loaded");
    var username = null;
    const userspan = document.getElementById('usernamespan');
    if (userspan) {
        username = userspan.dataset.username;
    }
    console.log("username:");
    console.log(username);

    // get info from localstorage
    var cart = JSON.parse(localStorage.getItem(username));
    if (!cart) {
        cart = {
            'count': 0,
            'items': {},
        }
    }
    if(cart.count) {
        updateCartCount(cart.count)
    }
    
    console.log("cart:");
    console.log(cart);
     
    //  bring up dialog to add to cart
    document.querySelectorAll('.menuitem').forEach(function(a) {
        a.addEventListener("click", function (event) {
            event.preventDefault();
            // when someone clicks on a price, check if logged in,
            if (typeof username === "undefined" || username === null) {
                alert("Must log in to add items to cart");
                // window.location.href = "login";
            } else {
                // check if already have active choice, if so, clean up
                if (activechoice) { cleanup() };
                // something's been chosen, so this should be true
                activechoice = true;
                // get info about what was clicked on
                const itemid = a.dataset.itemid;
                console.log("clicked on item with id:");
                console.log(itemid);
                const opts = a.dataset.opts;
                console.log("clicked on item with opts:");
                console.log(opts);
                const td = a.closest('td');
                td.className = "highlight";

                // template has buttons
                var source = document.getElementById("addcart-template").innerHTML;
                var template = Handlebars.compile(source);
                // initialize variable to hold html we'll build
                var optionshtml = "";
                // if need to pick options
                
                // ajax request for options for this item returns promise
                const optionspromise = getOptions(itemid, opts);
                optionspromise.then(p => {
                    console.log("got options:");
                    console.log(p);
                    
                    for (var i = 0; i < opts; i++) {
                        optionshtml += "<select class='optionselect' id='select" + i.toString() +"'>";
                        for (var j = 0; j < p.length; j++) {
                            optionshtml += "<option value='" + p[j] + "'>" + p[j] +"</option>";
                        }
                        optionshtml += "</select><br>";
                    }
                    
                    console.log("optionshtml:");
                    console.log(optionshtml);
                    
                    // finish creating text and insert
                    var htmlblock = template({selectforms: optionshtml});
                    console.log("htmlblock:");
                    console.log(htmlblock);
                    var div = document.createElement('div');
                    div.id="deleteme";
                    div.innerHTML = htmlblock;
                    var row = a.closest("tr");
                    row.insertAdjacentElement('afterend', div);

                    // add listener to cancel button
                    const cancelbutton = document.getElementById("cancelbutton");
                    cancelbutton.addEventListener("click", function (event) {
                        console.log("cancel clicked");
                        cleanup();
                        activechoice = false;
                    });

                    // add listener to add to cart button
                    const addtocartbutton = document.getElementById("addtocartbutton");
                    addtocartbutton.addEventListener("click", function (event) {
                        console.log("add to cart clicked");
                        // make cart item with menu item ID and options add to cart
                        var cart_item = { 
                            "id": itemid,
                            "options": null,
                        };
                        var options = document.getElementsByClassName('optionselect');
                        console.log("options");
                        console.log(options);
                        if (options.length) {
                            cart_item.options = options[0].value;
                            for (let i = 1; i < options.length; i++) {
                                cart_item.options += ", " + options[i].value
                            }
                        }
                        console.log("cart_item:");
                        console.log(cart_item);
                        cart.count += 1;
                        console.log("cart.count:");
                        console.log(cart.count);
                        cart.items[cart.count.toString()] = cart_item;
                        console.log("cart:");
                        console.log(cart);
                        localStorage.setItem(username, JSON.stringify(cart));
                        updateCartCount(cart.count)
                        cleanup();
                        activechoice = false;
                    });
                })
                

                

            }
        });

    });
    
});

function getOptions(itemid, opts) {
    console.log("getOptions called with id:");
    console.log(itemid)
    
    return new Promise(function (resolve, reject) {
        if (!opts) {
            resolve("");
        }
        const request = new XMLHttpRequest();
        request.open('POST', '/getoptions');
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

function cleanup() {
    console.log("cleanup called");
    
    // delete buttons and form
    var deletediv = document.getElementById("deleteme");
    deletediv.parentNode.removeChild(deletediv);
    // reset highlight
    var cells = document.getElementsByClassName("highlight");
    for (let cell of cells) {
        cell.classList.remove("highlight");
    };
}

function updateCartCount(count) {
    console.log("updateCartCount called")
    document.getElementById("cart_count").innerHTML = "(" + count.toString() + ")"
}