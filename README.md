# Additional Task 1

We've created 2 new methods on the server. One accepts a comment as sent by a user, and stores it on the server. The other lists all the comments that are currently stored in the system, and the name of the user who created it.

Feel free to compare the new `main.py` file with your version to see what changes have been made.

### Step 1
Alter the secure page so that a logged in user has a way to send comments to the server. The new endpoint requires a `POST` request to the server, and the endpoint is `/comments`. It expects form data with a field `comment`, of which should be the text content that the user sent.

You'll notice that when you send a comment to the server, the page refreshes, but you don't see the new comment being shown below to the `User comments will be shown below!` heading.

You can verify that the comments are being set to the server by visiting `/comments` from your browser, it'll show you the data that is currently stored on the server.

### Setp 2
Now that we know the comments are being stored on the server, let's update the page to show all the comments that have been sent in.

Inspect the html for the secure page, and write some JavaScript to `fetch` the comments stored on the server. This information can be retrieved from the server via a `GET` request to the `/comments` endpoint. 

If you need help, search for JavaScript fetch, ask one of the helpers, or ask one of your colleagues!