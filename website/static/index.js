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

function deletePost(postID) {
    fetch('/delete-post', {
        method: 'POST',
        body: JSON.stringify({ postID: postID})
    }).then((_res) => {
        window.location.href = "/view";
    });
}

function captureInput() {
    var email = document.forms["input"]["email"].value;
    var name = document.forms["input"]["firstName"].value;
    console.log(email);
    temp = email;
    console.log(temp)
    document.getElementById("firstName").value = name;
    document.getElementById("email").value = email;

}