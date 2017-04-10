from django.http import HttpResponse
import re
import requests
import os

class Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

        if os.environ["S4A_TOKEN"] is None:
            raise ValueError("Missing S4A_TOKEN environment variable.")

        self.baseUrl = "http://api.seo4ajax.com/" + os.environ["S4A_TOKEN"]


    def __call__(self, request):

        if request.method != 'GET' and request.method != 'HEAD':
            return self.get_response(request)

        if "_escaped_fragment_" in request.GET:
            return self.__serve(request)

        if re.match(r"(googlebot/|googlebot-mobile|yandexbot|pinterest.*ios|mail\.ru|seznambot|screaming)", request.META['HTTP_USER_AGENT'], re.I) is not None:
            return self.get_response(request)

        if re.match(r".*(\.[^?]{2,4}$|\.[^?]{2,4}?.*)", request.path) is not None:
            return self.get_response(request)

        if re.match(r"(bot|spider|pinterest|crawler|archiver|flipboardproxy|mediapartners|facebookexternalhit|quora|whatsapp)", request.META['HTTP_USER_AGENT'], re.I) is not None:
            return self.__serve(request)

        return self.get_response(request)

    def __serve(self, request):

        headers = request.META
        if headers.get("X_FORWARDED_FOR"):
            headers["X_FORWARDED_FOR"] = headers['REMOTE_ADDR'] + "," + headers["X_FORWARDED_FOR"]
        else:
            headers["X_FORWARDED_FOR"] = headers['REMOTE_ADDR']

        for header in headers:
            headers[header] = str(headers[header])

        try:
            request = requests.get(self.baseUrl + request.get_full_path(), headers=headers, allow_redirects=False)
            response = HttpResponse(content=request.text, status=request.status_code, content_type=request.headers['content-type'])

            if request.headers.get("x-powered-by"):
                response.setdefault("x-powered-by", request.headers["x-powered-by"])

            if request.headers.get("vary"):
                response.setdefault("vary", request.headers["vary"])

            if request.headers.get("last-modified"):
                response.setdefault("last-modified", request.headers["last-modified"])

            if request.headers.get("etag"):
                response.setdefault("etag", request.headers["etag"])

            if request.headers.get("cache-control"):
                response.setdefault("cache-control", request.headers["cache-control"])

            if request.headers.get("date"):
                response.setdefault("date", request.headers["date"])

            if request.headers.get("retry-after"):
                response.setdefault("retry-after", request.headers["retry-after"])

        except:
            response = HttpResponse(content="Temporary unavailable", status=503, content_type="text/html;")

        return response