# Additional Task 2

We've completed the steps for Additional Task 1. Both of the users can now send comments, and they are shown on the secure page just as we'd expect. Great!

Unfortunately, there are a couple of vulnerabilities in our implementation. Lets try and find them with Burp.

Restart your server, and visit your server in Burp's browser.

Login using Alice or Bob's credentials.

Navigate to the `Target` tool, and look in the `Issues` panel. You should see `TLC cookie without secure flag set`. Feel free to click on it, and read the details in the advisory tab, but this issue basically tells you that the cookie can be accessed using JavaScript. Keep this in mind.

### Main Exploit

Submit the comment `<img src=x onerror="alert('XSS Attack')">`.

The page will refresh, and you will see an alert saying XSS Attack.

This alert in itself is fairly harmless, but the JavaScript code that ran could have been anything, including stealing the logged in user's session cookie!

This would allow an attacker to impersonate another user, perform actions as if they were them.

In this example, if Bob was able to steal Alice's cookie, Bob could post comments on Alice's behalf.

It is paramount that user input is sanitised before being stored.

Submit the comment `<img src=x onerror="alert(document.cookie.toString())">`

You can see the user's cookie gets shown in the alert dialog.

Instead of just showing the cookie in an alert, an attacker could send the session id to themselves, and now they can impersonate the user.

### Partial Remediation

One way we could prevent the user's cookie from being accessed would be to make the session id cookie `HttpOnly`.

[This](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie) page has information on how to make a cookie `HttpOnly`. Proceed to alter the `main.py` file, and make our session id cookie `HttpOnly`.

Restart your server, and try to submit the comment `<img src=x onerror="alert(document.cookie.toString())">`

Now, you should see that you don't see the session id alerted to the user.

Although the cookie now can't be accessed using JavaScript directly anymore, the server is still vulnerable to XSS.