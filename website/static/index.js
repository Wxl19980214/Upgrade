var qrcode = new QRCode("qrcode");

$(document).ready(function() {

});

function showQrcode() {


    qrcode.makeCode("http://127.0.0.1:5000/home");
    $("#qrcont").show();
}


function showQrcode2(psid) {



    $("#qrcode").hide();
    qrcode.makeCode("http://127.0.0.1:5000/post/" + psid);
    $("#qrcode").show();
}


function closeQrcode() {
    $("#qrcont").hide();
}