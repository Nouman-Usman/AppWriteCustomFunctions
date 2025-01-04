from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
import os
import json

def handle_get(context, users):
    try:
        response = users.list()
        return context.res.json({
            "status": "success",
            "data": response,
            "message": "Users retrieved successfully"
        })
    except AppwriteException as err:
        context.error("GET request failed: " + repr(err))
        return context.res.json({
            "status": "error",
            "message": str(err)
        }, 500)

def handle_post(context, users):
    try:
        # Parse the JSON string into a dictionary
        data = json.loads(context.req.body)
        
        response = users.create(
            user_id='unique()',  # This is required by Appwrite
            name=data.get('Name'),
            phone=data.get('Phone'),
            email=data.get('email'),
            password=data.get('password')
        )
        return context.res.json({
            "status": "success",
            "data": response,
            "message": "User created successfully"
        })
    except json.JSONDecodeError as e:
        return context.res.json({
            "status": "error",
            "message": "Invalid JSON in request body"
        }, 400)
    except AppwriteException as err:
        context.error("POST request failed: " + repr(err))
        return context.res.json({
            "status": "error",
            "message": str(err)
        }, 500)

def handle_delete(context, users, user_id):
    try:
        response = users.delete(user_id)
        return context.res.json({
            "status": "success",
            "message": f"User {user_id} deleted successfully"
        })
    except AppwriteException as err:
        context.error("DELETE request failed: " + repr(err))
        return context.res.json({
            "status": "error",
            "message": str(err)
        }, 500)

def handle_put(context, users, user_id):
    try:
        data = context.req.body
        response = users.update_email(user_id, data.get('email'))
        return context.res.json({
            "status": "success",
            "data": response,
            "message": f"User {user_id} updated successfully"
        })
    except AppwriteException as err:
        context.error("PUT request failed: " + repr(err))
        return context.res.json({
            "status": "error",
            "message": str(err)
        }, 500)

def main(context):
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )
    users = Users(client)

    method = context.req.method
    path = context.req.path
    
    # Basic routing
    if path == "/ping":
        return context.res.text("Pong")
    if method == "GET":
        return handle_get(context, users)
    elif method == "POST":
        return handle_post(context, users)
    elif method == "DELETE":
        user_id = context.req.query.get('user_id')
        if not user_id:
            return context.res.json({"status": "error", "message": "user_id is required"}, 400)
        return handle_delete(context, users, user_id)
    elif method == "PUT":
        user_id = context.req.query.get('user_id')
        if not user_id:
            return context.res.json({"status": "error", "message": "user_id is required"}, 400)
        return handle_put(context, users, user_id)
    
    return context.res.json({
        "status": "error",
        "message": "Method not supported"
    }, 405)
