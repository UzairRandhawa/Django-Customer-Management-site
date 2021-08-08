var updateBtn = document.getElementsByClassName('update-cart')


for(var i =0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
         var productID = this.dataset.product
         var action = this.dataset.action
         console.log('productID', productID, 'action', action)
        
         

         console.log('User:', user)
         if(user === 'AnonymousUser'){
             console.log('User is not logged in....')
            addCookieItem(productID, action)
            }
        else{
            
            updateUserOrder(productID, action)
        }
    
    
    })
}


function addCookieItem(productId, action){
    
    if(action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
    
        }
        else{
            cart[productId]['quantity'] += 1
        }

    }
    if(action == 'remove'){
        
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item Should be deleted..')
            delete cart[productId];
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    
}


function updateUserOrder(productId, action){

    console.log('User is Authenticated, Sending data...')
    // var url = 'update_item/'

    fetch('/update_item/', {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFTOKEN' : csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})

    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('Data:', data)
        location.reload()
    })
}