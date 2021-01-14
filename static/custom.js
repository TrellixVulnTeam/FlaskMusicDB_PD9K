$("document").ready(function(){
    $("advanced-search").hide();
});

$('.simple-search-btn').click(function(e) {
    e.preventDefault();
    $('.simple-search').show();
    $('.advanced-search').hide();
  });

$('.advanced-search-btn').click(function(e) {
    e.preventDefault();
    $('.advanced-search').show();
    $('.simple-search').hide();
});
