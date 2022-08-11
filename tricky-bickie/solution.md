# Tricky Bickie

## Problem

Once you successfully complete this challenge you'll come across a string in this format: PlexTrac_CTF=string. This is NOT the flag for points.

## Links

* https://tricky.plexhax.com

## Notes

The link goes to a login page, asking for a username and password.  Another button goes to signing up.  Looking at the source this entire page is just an HTML from pointing to a PHP backed.  Both the login and sign up forms are part of the login, so signing up doesn't actually work.  Both forms hit the login.php route.

While the route could be looked at, another thing to note is that the site does put a cookie into my browser, this cookie name is "isauth" and the value is "ZmFsc2U=", if this cookie can be decrypted than we could generate the correct cookie and use that to auto login.

The route doesn't look too special, it takes form data and if I try requesting the header I don't see anything special about it.

The cookie on the other hand sticks out to being the solution.  The cookie is only a few characters, and converting those characters from base64 shows the string "false".  The site tool [CyberChef](https://cyberchef.org/) was used to convert from Base64.  Converting the string "true" to base 64 gives a encoded string "dHJ1ZQ==" which can be added to the cookie in Firefox. 

## Solution

Replacing the cookie with the new Base64 encoded string takes us to a new page https://tricky.plexhax.com/youresocoolyourewinning.html, with the flag shown.  The flag is PlexTrac_CTF=clout_forest_gum_scout

