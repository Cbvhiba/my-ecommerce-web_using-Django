$(document).ready(function(){
     $('#rzp-button1').click(function(e){
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var country = $("[name='country']").val();
        var state = $("[name='state']").val();
        var city = $("[name='city']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (fname == "" || lname == "" || email == "" || phone == "" || address == "" || country == "" || state == "" || city == "" || pincode == "")
        {
            swal("Alert ", "All fields are mandatory", "error");
            return false;
        }
        else{
            $.ajax({
                method: "GET",
                url: "/accounts/proceedtopay/",
                success: function (response) {
                    console.log(response);

                    var options = {
                        "key": "rzp_test_oRfSzsSGPgUAwU",
                        "amount": response.total_price * 100,
                        "currency": "INR",
                        "name": "Ecomm_pro",
                        "description": "Thanyou for buying from us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "{{payment.id}}",
                        "handler": function(responseb){
                            // window.location.href = `http://127.0.0.1:8000/accounts/success/?razorpay_payment_id=${response.razorpay_payment_id}&razorpay_order_id=${response.razorpay_order_id}&razorpay_signature=${response.razorpay_signature}`
                            alert(responseb.razorpay_payment_id);
                            // alert(response.razorpay_order_id);
                            // alert(response.razorpay_signature);
                            data = {
                                "fname": fname,
                                "lname": lname,
                                "email": email,
                                "phone": phone,
                                "address": address,
                                "country": country,
                                "state": state,
                                "city": city,
                                "pincode": pincode,
                                "payment_mode": "paid by razorpaay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method: "POST",
                                url: "{% url 'placeorder' %}",
                                data: data,
                                success: function (responsec){
                                    swal("Congratulation", responsec.status, "success").then((value) => {
                                        window.location.href = '/accounts/your_orders'
                                    });
                                }
                            });
                        },
                        "prefill": {
                            "name": fname+" "+lname,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    // var rzp1 = new Razorpay(options);
                    // rzp1.on('payment.failed', function(response){
                    //     alert(response.error.code);
                    //     alert(response.error.description);
                    //     alert(response.error.source);
                    //     alert(response.error.step);
                    //     alert(response.error.reason);
                    //     alert(response.error.metadata.order_id);
                    //     alert(response.error.metadata.payment_id);
                    // });

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
        }
     });
});