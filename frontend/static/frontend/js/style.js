jQuery(document).ready(function($) {
  var alterClass = function() {
    var ww = document.body.clientWidth;
    if (ww < 500) {
      $('#footer').removeClass('p-5');
      $('#footer-logo').removeClass('p-5');
      $('#footer-items').removeClass('p-5');
      $('.navbar').removeClass('pl-5');
      $('.navbar').removeClass('pr-5');
    } else if (ww >= 501) {
      $('#footer').addClass('p-5');
      $('#footer-logo').addClass('p-5');
      $('#footer-items').addClass('p-5');
      $('.navbar').addClass('pl-5');
      $('.navbar').addClass('pr-5');
    };
  };
  $(window).resize(function(){
    alterClass();
  });
  //Fire it when the page first loads:
  alterClass();
});



