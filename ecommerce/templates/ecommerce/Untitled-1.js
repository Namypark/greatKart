
<script>
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var amount = {{total}}
const csrftoken = getCookie('csrftoken');
var order_id = {{order.order_id}}
var payment_method = 'PayPal';
var url = "{% url 'payments' %}";

  // Render the PayPal button into #paypal-button-container
  paypal.Buttons({
    
    style: {
      color:  'black',
      shape:  'pill',
      label:  'pay',
      height: 40
  },
    
    // Set up the transaction
    createOrder: function(data, actions) {
      return actions.order.create({
          purchase_units: [{
              amount: {
                  value: amount,
              }
          }]
      });
  },
  

  // Finalize the transaction
  onApprove: function(data, actions) {
      return actions.order.capture().then(function(orderData) {
          // Successful capture! For demo purposes:
          //console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
          console.log(orderData)
          var transaction = orderData.purchase_units[0].payments.captures[0];

          function sendData(){
            fetch(url, {
              method="POST",
              header = {
                'content-type': 'application/json',
                'X-CSRFToken': csrftoken,
              },
              body: JSON.stringify(
                {
                  orderID: order_id,
                  transID: orderData.id,
                  payment_method:payment_method,
          
                }
              )
            })
            //.then(response => response.json())
            //.then(orderData => 'success:',orderData)
          }
          //alert('Transaction '+ transaction.status + ': ' + transaction.id + '\n\nSee console for all available details');

          // Replace the above to show a success message within this page, e.g.
          const element = document.getElementById('paypal-button-container');
          element.innerHTML = '';
          element.innerHTML = '<h3>Thank you for your payment!</h3>';
          // Or go to another URL:  actions.redirect('thank_you.html');
      });
  }
  

  }).render('#paypal-button-container');