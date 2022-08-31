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
            console.log('Not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    })
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