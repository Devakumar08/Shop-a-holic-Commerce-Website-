$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function() {
    console.log("Plus Clicked");
    var id = $(this).attr("pid").toString(); // Use `find('i')` to locate the <i> element
    var eml = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id // Use a colon (:) for key-value pairs
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount

            document.getElementById("total_amount").innerText = data.total_amount
        }
    });
});

$('.minus-cart').click(function() {
    console.log("Plus Clicked");
    var id = $(this).attr("pid").toString(); // Use `find('i')` to locate the <i> element
    var eml = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id // Use a colon (:) for key-value pairs
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount

            document.getElementById("total_amount").innerText = data.total_amount
        }
    });
});
$('.remove-cart').click(function() {
    console.log("Remove Clicked");
    var id = $(this).attr("pid");
    var eml = this
        // console.log(id);
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("Item removed");
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("total_amount").innerText = data.total_amount;
            // You might also want to remove the HTML element of the item from the cart view
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    });
});