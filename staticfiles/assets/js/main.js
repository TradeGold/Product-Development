

$(function () {
    $(".choice").find("button").hide(0);
    $(".nav-link").click(function () {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });

    $(".dropdown").hover(function () {
        $(this).find(".dropdown-menu").show(0);
    }, function () {
        $(this).find(".dropdown-menu").hide(0);
    });

    $(".small-product").click(function () {
        $("#mainproduct").attr("src", $(this).attr('src'))
    });

    $(".choice").hover(function(){
        $(this).find("button").show(0);
    }, function(){
        $(this).find("button").hide(0);
    });

   
// For owl carousel
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:false,
        autoplay:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1000:{
                items:3
            }
        }
    });
    //For Faq Question




var incrementQty;
var decrementQty;
var plusBtn  = $(".qtyadd");
var minusBtn = $(".qtysub");
var incrementQty = plusBtn.click(function() {
    var $n = $(this)
    .parent(".button-container")
    .find(".quantity");
    $n.val(Number($n.val())+1 );
    update_amounts();
});

update_amounts();
var decrementQty = minusBtn.click(function() {
    var $n = $(this)
    .parent(".button-container")
    .find(".quantity");
    var QtyVal = Number($n.val());
    if (QtyVal > 1) {
        $n.val(QtyVal-1);
    }
    update_amounts();

});

var current_fs, next_fs, previous_fs; //fieldsets
        var opacity;

        function nextpage(current_fs, next_fs) {


            //Add Class Active
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

            //show the next fieldset
            next_fs.show();
            //hide the current fieldset with style
            current_fs.animate({ opacity: 0 }, {
                step: function (now) {
                    // for making fielset appear animation
                    opacity = 1 - now;

                    current_fs.css({
                        'display': 'none',
                        'position': 'relative'
                    });
                    next_fs.css({ 'opacity': opacity });
                },
                duration: 600
            });
        };

        $(".next").click(function () {
            current_fs = $(this).parent();
            next_fs = $(this).parent().next();
            nextpage(current_fs, next_fs);
        });

        $(".validatedelivery").click(function () {
            var name = $("input[name=fullname]").val();
            var address = $("input[name=dAddress]").val();
            var dDate = $("input[name=dDate]").val();
            var phno = $("input[name=phno]").val();

            if (name == "" || address == "" || dDate == "" || phno == "") {
                $("#deliveryInformationError").html("*Please fill all fields");
            } else {
                if (phno.length == 10 && isNaN(phno) == false) {
                    $("#deliveryInformationError").html("");
                    current_fs = $(this).parent();
                    next_fs = $(this).parent().next();
                    nextpage(current_fs, next_fs);
                } else {
                    $("#deliveryInformationError").html("*Please Enter Valid Phone No.");
                }
            }

        });

        $(".validatepayment").click(function () {

                current_fs = $(this).parent();
                next_fs = $(this).parent().next();
                nextpage(current_fs, next_fs);

        });



        $(".previous").click(function () {

            current_fs = $(this).parent();
            previous_fs = $(this).parent().prev();

            //Remove class active
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

            //show the previous fieldset
            previous_fs.show();

            //hide the current fieldset with style
            current_fs.animate({ opacity: 0 }, {
                step: function (now) {
                    // for making fielset appear animation
                    opacity = 1 - now;

                    current_fs.css({
                        'display': 'none',
                        'position': 'relative'
                    });
                    previous_fs.css({ 'opacity': opacity });
                },
                duration: 600
            });
        });
    

});
function update_amounts(){
    var sum = 0.0;
    
    $('#myTable > tbody  > tr').each(function() {
        
        var qty = $(this).find('.quantity').val();
        var price = $(this).find('.unitprice').html();
        var amount = (qty*price)
        sum+=amount;
        $(this).find('.amount').html(amount);
    });
    $('.total').text(sum);

   
}






