// This file contains cart functionalities

// console.log('Loading :)');

let updateBtns = document.getElementsByClassName('update-cart');

for(let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if(user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    })
}

// Function allowing not authenticated user to add or remove items to their cart 
// and store the items in cookies
function addCookieItem(productId, action) {
    console.log('User is not logged in');

    if(action == 'add') {
        // If cart item is not added, add it and if it is, increase its value
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
        } else {
            cart[productId]['quantity'] += 1; 
        }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1;
        if(cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";admin=;path=/";
    // location.reload() is used to display the cart update next to the cart icon
    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    // This variable defines view in which our data will be displayed
    let url = '/update_item/';

    // Fetch call sends data to the back end to our view
    // The first thing passed to the fetch function is url and then we need to define
    // what kind of data needs to be passed
    // Since we're passing POST data, we need to pass headers too
    // Here, headers are an object
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // Once we passed the headers, we need to send the body which is data we're sending
        // to the back-end - it needs be send as an object but to do this this way, we have 
        // to stringify it, so it passes as a string
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    // This next fragment collects the data and make it to JSON again
    .then((response) => {
        return response.json();
    })
    // While this function just consoles out the data
    .then((data) => {
        console.log('Data:', data);
        location.reload();
    })
}