from flask import jsonify

def handle_not_found_error(error):
    """ Reformats the not found error"""
    response = jsonify({
        "success": False,
        "error": 404,
        "message": str(error.description) if hasattr(error, 'description') else "Resource not found"
    })
    return response, 404

def handle_bad_request(error):
    """ Reformats the Bad Request Error """
    response = jsonify({
        "success": False,
        "error": 400,
        "message": str(error.description) if hasattr(error, 'description') else "Bad Request"
    })
    return response, 400


def handle_server_error(error):
    """ Reformats the Server Error """
    response = jsonify({
        "success": False,
        "error": 500,
        "message": str(error.description) if hasattr(error, 'description') else "Internal Server Error"
    })
    return response, 500

def register_error_handlers(app):
    """ Registers all error in the application """
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(500, handle_server_error)
