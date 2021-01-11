$(document).ready(function () {
  $(window).scroll(function (event) {
    var y = $(this).scrollTop();
    if (y >= 100) {
      $(".home-nav").addClass("blue-nav");
    } else {
      $(".home-nav").removeClass("blue-nav");
    }
  });
});
