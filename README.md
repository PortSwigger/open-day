# Web Server Exercise

The aim of this exercise is to familiarize yourself with HTTP requests and responses, and take a look at some basic authentication mechanisms for logging into websites.
In this repository, you can find a basic implementation of a web server written in Python. It is incomplete, and will need the functionality described in the comments implemented.

As part of this, you will also get the chance to use our product, Burp Suite Professional.

## Steps
1. Launch the web server, and access the root page through Burp's built-in browser.
2. Attempt to log in with the username and password: `alice : 1234`
   - What issues do you encounter at this point? Which method do you think you will need to implement first?
3. Are we able to access the `/secure` endpoint when not logged in? How could we prevent this?
   - When logging in, how do we identify to the web server that we are a valid user?
   - How can we prevent access to the endpoint when not authenticated? Are there any error messages that we can use?
4. Use Burp to add a fake cookie in Repeater to gain access to `/secure`
5. When we log out from the site, how do we prevent our cookie from staying in our session?
   - [Spoiler](https://stackoverflow.com/questions/5285940/correct-way-to-delete-cookies-server-side)!

## Additional:
1. Open the "Additional" project.
1. I'd like to be able to log in with the user `bob` as well.
   - How does the web server identify individual users?
2. Create a form to submit plaintext comments to the page.
3. Be able to view comments.
4. Is there a way that we can exploit this comment functionality to steal cookies from users?
   - https://portswigger.net/web-security/cross-site-scripting#stored-cross-site-scripting

### Completely done?
Provide some styling to the site.