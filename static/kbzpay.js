import {QRCode} from './qrcodejs/qrcode.js';

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#paynow').addEventListener('click', () => paynow())
})

function paynow() {
  fetch('/', {
    method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)

    var qrcode = new QRCode(document.getElementById("qrcode"))
    var checkout = document.getElementById('checkout')
    checkout.style.display = "none"
    qrcode.makeCode(data['qrc'])

  })

}
