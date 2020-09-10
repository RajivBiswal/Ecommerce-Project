  $(document).ready(function(){
    var productForm = $(".form-product-ajax")
    productForm.submit(function(event){
      event.preventDefault();
      var thisForm = $(this)
      // var actionEndpoint = thisForm.attr("action");
      var actionEndpoint = thisForm.attr("data-end-point");
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find(".submit-span")

          if(data.added){
            submitSpan.html("<button type='submit' class='btn btn-link'>Remove?</button>")
          }
          else{
            submitSpan.html("<button type='submit' class='btn btn-success'>Add To Cart</button>")

          }
          var cartCount = $(".cart-item-count")
          cartCount.text(data.totalItemsCount)
          var currentPath = window.location.href
          if(currentPath.indexOf('cart') != -1){
              refreshCart()
          }
        },
        error: function(errorData){
          $.alert({
            title:"Oops!!",
            content:"An Error occoured",
            theme: "modern",
          })
        }
      })
    })
  function refreshCart(){
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    // cartBody.html("<h1>Changed</h1>")
    var productRows = cartBody.find(".cart-product")
    var currentUrl = window.location.href

    var refreshCartUrl = 'api/cart';
    var refreshCartMehtod = 'GET';
    var data = {};

    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMehtod,
      data: data,
      success: function(data){
        var hiddenCartItemRemove = $(".cart-item-remove")
        if (data.products.length > 0){
          productRows.html("")
          i = data.products.length

          $.each(data.products, function(index,value){
            var newCartItemRemove = hiddenCartItemRemove.clone()
            newCartItemRemove.css("display","block")
            newCartItemRemove.find(".cart-item-product-id").val(value.id)
            cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newCartItemRemove.html() + "</td>"+"<td>"+value.price +"</td></tr>")
            i--
          })
          cartBody.find(".cart-subtotal").text(data.subtotal)
          cartBody.find(".cart-total").text(data.total)
        }
        else {
          window.location.href = currentUrl
        }
      },
      error: function(errorData){
        $.alert({
          title:"Oops!!",
          content:"An Error occoured",
          theme: "modern",
        })
      }
    })
  }
  })

  // Auto Search with JQuery
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']")
  var typingTimer;
  var typingInterval = 500
  var searchBtn = searchForm.find("[type='submit']")
  searchInput.keyup(function(event){
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch,typingInterval)
  })
  searchInput.keydown(function(event){
    clearTimeout(typingTimer)
  })

  function performSearch(){
    searchBtn.addClass('disabled')
    searchBtn.html("<i class='fa fa-spinner'</i> Searching...")
    var query = searchInput.val()
    setTimeout(function(){
      window.location.href = '/search/?q=' + query
    }, 1000)

  }
