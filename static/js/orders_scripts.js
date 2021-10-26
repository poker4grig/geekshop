window.onload = function () {

    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    console.log(TOTAL_FORMS)


    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;


    for (let i=0; i < TOTAL_FORMS; i++) {
       _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
       _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
       console.log(_price)
       quantity_arr[i] = _quantity;
       if (_price) {
           price_arr[i] = _price;
       } else {
           price_arr[i] = 0;
       }
    }

    console.info('PRICE', price_arr)
    console.info('QUANTITY', quantity_arr)
}