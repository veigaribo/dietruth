from core.util import get_session

# Stores the previous URL the user accessed in session
def previous_url_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        session = get_session(request)
        session["previous_url"] = request.build_absolute_uri()

        return response

    return middleware
