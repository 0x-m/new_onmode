
function like(elem) {
    const product_id = elem.dataset['pid'];
    fetch('/catalogue/product/' + product_id + '/' + 'like').then(res => {
        if (res.status == 200) {
            res.json().then(data => {
                if (data['status'] == 'liked'){
                    elem.classList.add('bg-red-500');
                    elem.classList.add('text-white');
                }
                else if(data['status'] == 'unliked') {
                    elem.classList.remove('bg-red-500');
                    elem.classList.remove('text-white')
                    
                }
            });
        }   
        else {

        }
    });
}

function addToCart(elem) {
    const product_id = elem.dataset['pid'];
    const collection = elem.dataset['collection'] ?? '';
    const obj = document.getElementById('product_options');
    const options = obj == null ? '': obj.value;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log(csrf_token);
    elem.disabled = true
    fetch('/cart/add', {
        method: 'POST',
        body: new URLSearchParams({
            product: product_id,
            quantity: 1,
            collection:  collection ,
            options: options
        }),
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then((res) => {
        if (res.status == 200) {
            elem.disabled = false;
        }
        console.log(res)
    });

}

function deleteFromCart(elem) {
    const order_item_id = elem.dataset['itemid'];
    const final_price = document.getElementById('final_price');
    fetch('/cart/delete/' + order_item_id).then((res) => {
        if (res.status == 200) {
            res.json().then(json => {
                final_price.innerText = json['final_price'];
            });
            elem.parentNode.remove();
        }
    });


}

function applyCoupon(elem) {
    const order_id = elem.dataset['order'];
    const coupon_code = document.getElementById('coupon_code').value;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const final_price = document.getElementById('final_price');
    const delete_coupon_template = document.getElementById('delete_coupon_template');
    const has_coupon = document.getElementById('has_coupon');

    elem.disabled = true;
    fetch('/cart/coupon/add', {
        method: 'POST',
        body: new URLSearchParams({
            code: coupon_code,
            order_id: order_id
        }),
        headers:{
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded'

        }
    }).then((res) => {
        if (res.status == 200) {
            res.json().then(data => {
                final_price.innerText = data['final_price'] + 'تومان';
                elem.parentNode.parentNode.replaceChildren(delete_coupon_template.content.cloneNode(true));
                has_coupon.innerText  = 'دارد';
            });
        }
        else{
            document.getElementById('coupon_error_text').classList.remove('hidden');
        }
        elem.disabled = false
    });

}

function deleteCoupon(elem) {
    const order_id = elem.dataset['order'];
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const final_price = document.getElementById(elem.dataset['final_price']);
    const add_coupon_template = document.getElementById('add_coupon_template');
    const has_coupon = document.getElementById('has_coupon');
    fetch('/cart/coupon/delete', {
        method: 'POST',
        body: new URLSearchParams({
            order_id: order_id
        }),
        headers:{
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded'

        }
    }).then((res) => {
        if (res.status == 200) {
            res.json().then(data => {
                final_price.innerText = data['final_price'] + 'تومان';
                elem.parentNode.replaceChildren(add_coupon_template.content.cloneNode(true));
                has_coupon.innerText = 'ندارد';
            });
        }
        else {
            // console.log('invalid coupon');
            // document.getElementById("coupon_error_text").classList.remove('hidden');
            
        }
    })
}

function incrementQuantity(elem) {
    const order_item_id = elem.dataset['itemid'];
    const final_price = document.getElementById(elem.dataset['total']);
    const num_box = elem.nextElementSibling;
    elem.disabled = true;
    fetch('/cart/increment/' + order_item_id).then((res) => {
        if (res.status == 200) {
            res.json().then((json) => {
                final_price.innerText = json['final_price'];
                num_box.value = parseInt(num_box.value) + 1
            });
            elem.disabled = false;
        }
    });
}

function decrementQuantity(elem) {
    const order_item_id = elem.dataset['itemid'];
    const final_price = document.getElementById(elem.dataset['total']);
    const num_box = elem.previousElementSibling;
    elem.disabled = true;
    fetch('/cart/decrement/' + order_item_id).then((res) => {
        if (res.status == 200) {
            res.json().then(json => {
                final_price.innerText = json['final_price'];
                num_box.value = parseInt(num_box.value) - 1;
                if (num_box.value == 0) {
                    elem.parentNode.parentNode.remove();
                }
            });
            elem.disabled = false;
        }
    });
}
