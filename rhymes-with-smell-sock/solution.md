# Rhymes with: Smell Sock

## Problem

The file smellsock.txt on the host https://smelly.plexhax.com contains the password to unzip the attached zip file.

## Links

* https://smelly.plexhax.com/

## Notes

This prompt sounds like its implying that if I know where the file is on the system, I can path to it in the URL and download it.  The site shows off a the debug page for an apache webserver, this baits the idea that this site is a simple apache server not locked down.  This means that config settings, random text files in /var/www, etc can all be found if we know the file paths, and the names of the files.  Some commnon names of files for an apache webserver can be.

* .htaccess
* robots.txt
* .DN_Store (if it's a Mac)

In this case, the .htaccess file is present, but the server forbids us from viewing it.  So far no file, including smellsock.txt can be found, and this may play into the name of the CTF, the name of the file is a rhyme of smell sock.  I could create a list of words that rhyme with smell and sock, but this would be a very manual way of solving this problem.

## Gobuster

[Gobuster Tutorial](https://hackertarget.com/gobuster-tutorial/) may be a way to solve this problem.  I have heard of Gobuster before when doing a similar problem on PicoCTF, but the CTF was found in one of the common files listed above.  Gobuster is aggressive, and it could be way to brutish on its own to warrent using it for this puzzle.  But we could make it less aggressive by providing it the word list we create made up of words that ryhme with smell and sock.  Providing that ourselves, it justifies the use of Gobuster as a tool that handles the repretition of iteratering through the word list.

Plus how many times are you given the opportunity to try out these tools *legally*, it's good practice.

## Solution

Answer
