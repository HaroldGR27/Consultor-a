
src = "https://www.paypal.com/sdk/js?client-id=AayTGTNUMpgA5wSS8tnVzJMirQj5XowP7KIDukp2LxfEXxcrO0-AbRb1RCAED2Kmxc-GGnzsenYov0UZ" >


    paypal.Buttons({
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: '0.01'
                    }
                }]
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                alert('Transaction completed by ' + details.payer.name.given_name);
            });
        }
    }).render('#paypal-button-container')
