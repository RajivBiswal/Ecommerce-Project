$(document).ready(function(){
  var stripeFormModule = $(".stripe-payment-form")
      var stripeModuleToken = stripeFormModule.attr("data-token")
      var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
      var StripeModuleBtnTitle = stripeFormModule.attr("data-btn-title")

      var stripeTemplate = $.templates("#stripeTemplate")
      var stripeTemplateContext = {
          publishKey: stripeModuleToken,
          nextUrl: stripeModuleNextUrl,
          btnTitle: StripeModuleBtnTitle || 'Add New Card'
      }
      var stripeTemplateHtml = stripeTemplate.render(stripeTemplateContext)
      stripeFormModule.html(stripeTemplateHtml)

      var paymentForm = $(".payment-form")
      if (paymentForm.length > 1){
        alert("Only one payment form is allowed per page")
        paymentForm.css('display','none')
      }
      else if (paymentForm.length == 1){
        var pubKey = paymentForm.attr('data-token')
        var nextUrl = paymentForm.attr('data-next-url')
        // Set your publishable key: remember to change this to your live publishable key in production
        // See your keys here: https://dashboard.stripe.com/account/apikeys
        var stripe = Stripe(pubKey);
        var elements = stripe.elements();
        // Custom styling can be passed to options when creating an Element.
        var style = {
          base: {
            // Add your base input styles here. For example:
            fontSize: '16px',
            color: '#32325d',
            lineHeight: '24px',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            '::placeholder':{
              color: '#aab7c4'
            }
          },
          invalid: {
            color: '#fa755a',
            iconColor: 'fa755a'
          }
        };

        // Create an instance of the card Element.
        var card = elements.create('card', {style: style});

        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');

        card.addEventListener('change',function(event){
          var displayError = document.getElementById('card-errors');
          if (event.error){
            displayError.textContent = event.error.message;
          }
          else {
            displayError.textContent = '';
          }
        });

        // Create a token or display an error when the form is submitted.
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function(event) {
          event.preventDefault();

          stripe.createToken(card).then(function(result) {
            if (result.error) {
              // Inform the customer that there was an error.
              var errorElement = document.getElementById('card-errors');
              errorElement.textContent = result.error.message;
            } else {
              // Send the token to your server.
              stripeTokenHandler(nextUrl, result.token);
            }
          });
        });
        function redirectToNext(nextPath, timeoffset){
          if (nextPath){
            setTimeout(function(){
              window.location.href = nextPath
            },timeoffset)
          }
        }

        function stripeTokenHandler(nextUrl,token){
          //console.log(token.id)
          var paymentMethodEndpoint = '/billing/payment-method/create'
          var data = {
            'token': token.id
          }
          $.ajax({
            data: data,
            url: paymentMethodEndpoint,
            method: 'POST',
            success: function(data){
              var successMsg = data.message || "Your card is added successfuly!"
              card.clear()
              if(nextUrl){
                successMsg = successMsg + "<br><i class='fa fa-spin fa-spinner'></i>Redirecting..."
              }
              if ($.alert){
                $.alert(successMsg)
              }
              else{
                alert(successMsg)
              }
              redirectToNext(nextUrl, 1500)
            },
            error: function(error){
              console.log(error)
            }
          })
        }

      }
})
