$(function () {
  $("#go-fullscreen").click(function (e) { 
    e.preventDefault();
    
    $("#bigram-iframe").css({height:"95vh",width:"100vw",position:"fixed",left:"0", top:"0",zIndex:"10"})

    $("#close-fullscreen").removeClass("is-hidden");
  });

  $("#close-fullscreen").click(function (e) { 
    e.preventDefault();
    $("#bigram-iframe").css({height:"100%",width:"100%",position:"unset",left:"unset", top:"unset",zIndex:"unset"})
    $("#close-fullscreen").addClass("is-hidden");
  });

  $("#bigram-button").click(function (e) { 
    e.preventDefault();
    $("#bigram-iframe").attr("src",$("#bigram-select").val());
    $("#bigram-title").html($(`option[value='${$("#bigram-select").val()}']`).html());
  });
});
