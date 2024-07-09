var page = require('webpage').create();
page.open('http://10.0.1.1', function(status) {
  // console.log("Status: " + status);
  if(status === "success") {
    // Success!
  }
  phantom.exit();
});
