from flask import request


def get_request_data():
    """
    Get keys & values from the request.
    Parses requests with content type "application/x-www-form-urlencoded".

    Returns:
        dict: A dictionary with keys and values from the request.
    """
    try:
        # Ensure the request content type is "application/x-www-form-urlencoded"
        if request.content_type == "application/x-www-form-urlencoded":
            # Retrieve form data as a dictionary
            data = request.form.to_dict()
            return data
        else:
            raise ValueError("Invalid content type. Expected 'application/x-www-form-urlencoded'.")
    except Exception as e:
        # Handle any exceptions and log them if needed
        print(f"Error parsing request data: {e}")
        return {}
