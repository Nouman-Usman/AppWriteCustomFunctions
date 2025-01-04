from appwrite.client import Client
import os


# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    # Why not try the Appwrite SDK?
    #
    # Set project and set API key
    # client = (
    #     Client()
    #        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #        .set_key(context.req.headers["x-appwrite-key"])
    # )

    # You can log messages to the console
    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `context.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `context.res.text()` dispatches a string back to the client
        return context.res.text("Hello, World!")

    # `context.res.json()` is a handy helper for sending JSON
    return context.res.json({
        "motto": "Ok",
        "learn": "https://appwrite.io/docs",
        "connect": "https://appwrite.io/discord",
        "getInspired": "https://builtwith.appwrite.io",
    })
