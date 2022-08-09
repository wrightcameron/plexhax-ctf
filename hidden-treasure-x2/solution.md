# Hidden Treasure x 2

## Problem

No prompt, just this "Once you succesfully complete this challange you'll come across a string in this format: PlexTrac_CTF=string. This is NOT the flag for points."

And a link to site https://hidden.plexhax.com/

## Links

* https://hidden.plexhax.com/

## Notes

Clicking on the site leads to a plain text page that just says "yep".  Viewing page source the document isn't even HTML, but a plain text file with only "yep".  The Firefox debugger doesn't show much either with no Javascript present, no cookies either.

Looking at the response, there is a Response header called ETag, with value "617a7a03-4".  The [ETag is an offical HTML header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag), but I don't see it comanlly used, so its worth investigation see if it can be decrypted.

The value "617a7a03-4" looks to be hex.  Though converting it to ascii doesn't show anything special, just reads "azz..".  This doesnt tell me much, and there isn't any reverse search of this meaning.

There is another header included, the last modified time.

I don't have a lead at the moment 

### Hint 

The first hint just says, "dirb".  That sucks, I was already using the dirb tool to Web Content Scan the "Rhymes with: Smell Sock."  I could have used dirb before using the hint.

### Dirb

With dirb using the common.txt wordlist, the directory and file /register/index.php.  Checking out the index.php file, surprise it doesn't have php but this message.

```text
GET IS NOT the correct request method!

Parameter NULL. Keep Trying
```

Using postman the request type can be changed.  Changing the request type to POST, the response from the website was,

```html
<p>POST is correct request method! Closer you are... closer still.</p>
<p> Parameter NULL. Keep Trying</p>
```

Adding URL parameters or adding a json body didn't show the flag.  But I changed the request type to OPTIONS and using that the flag was shown in plain text.

## Solution

Using dirb the file /register/index.php is shown.  With a GET request this file returns a plain text file saying to use a POST request.  Using POST request says were close, but actually the OPTIONS request shows the flag in plain text.

Flag: PlexTrac_CTF=nominal_freelance_harps
Answer
