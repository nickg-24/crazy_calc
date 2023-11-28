Access Webserver Through HTTPS Reverse Proxy: https://{HOST_IPADDR}/calculator.html
Access Webserver Through ModSec Proxy: http://{HOST_IPADDR):8080/calculator.html
You can confirm modsec is running by attempting an XSS attack with the following parameters:
- Name: "<script>alert(1)</alert>
- number1: "1"
- operation: "+"
- number2: "2"

Instead of executing the javascript, users will be shown a "Forbidden" Page
