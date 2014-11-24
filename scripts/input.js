        $(document).ready(function() {
              // set max to length of wall (inches)
              // set min to 0 inches
              // set step equal to max (inches)
        
             $( "#wall_left" ).slider({ orientation: "vertical" ,
                                        range: true});
             $( "#wall_up" ).slider({ orientation: "horizontal" });
             $( "#lon").text("lon");
           });