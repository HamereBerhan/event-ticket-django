function domReady(fn) {
	if (
	  document.readyState === "complete" ||
	  document.readyState === "interactive"
	) {
	  setTimeout(fn, 1000);
	} else {
	  document.addEventListener("DOMContentLoaded", fn);
	}
  }
  
  domReady(function () {
	function onScanSuccess(decodeText, decodeResult) {
		document.getElementById('result').innerHTML = 'Your QR code is: ' + decodeText;
		document.getElementById('scanned_text').value = decodeText; // Update hidden form field
		var form = document.getElementById('qr-code-form');

// Submit the form
		form.submit();
	  
		// Submit the form using AJAX
		// (Code for sending AJAX request omitted for brevity)
	  }
  
	let htmlscanner = new Html5QrcodeScanner(
	  "my-qr-reader",
	  { fps: 10, qrbos: 250 }
	);
	htmlscanner.render(onScanSuccess);
  });