class ResponseEndpointsUtils:
    
    status_success = 'success'
    status_error = 'error'

    def create_message_endpoint_response(status, message):
        response = {
            "status": status,
            "message": message
        }

        return response