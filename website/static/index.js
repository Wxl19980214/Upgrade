
var qrcode = new QRCode("qrcode");

$(document).ready(function() {

});

function showQrcode() {


    qrcode.makeCode("http://127.0.0.1:5000/home");
    $("#qrcode").show();
}

