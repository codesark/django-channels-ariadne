from typing import Callable

from ariadne import format_error
from ariadne.asgi import GraphQL
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension
from ariadne.graphql import GraphQLError
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import URLRouter  # , ProtocolTypeRouter
from django.conf import settings
from django.urls import path, re_path

from api.schema import schema


class DjangoChannelsGraphQL(GraphQL):
    def __call__(self, scope) -> Callable:
        async def handle(receive, send):
            await super(DjangoChannelsGraphQL, self).__call__(scope, receive, send)
        return handle


def get_context_value(request):
    return {
        "request": request,
        "cookies": request.scope.get("cookies", {}),
        "user": request.scope.get("user"),
        "session": request.scope.get("session")
    }


def get_extensions(request, context):
    ext = []
    if settings.DEBUG:
        ext.append(ApolloTracingExtension)
    return ext


def extended_format_error(error: GraphQLError, debug: bool = False) -> dict:
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    formatted["message"] = "INTERNAL SERVER ERROR"

    return formatted


application = AuthMiddlewareStack(
    URLRouter([
        path("graphql/", DjangoChannelsGraphQL(
            schema,
            debug=settings.DEBUG,
            context_value=get_context_value,
            extensions=get_extensions,
            error_formatter=extended_format_error
        )
        ),
        re_path(r"", AsgiHandler),
    ], )
)


# application = ProtocolTypeRouter(
#     {
#         "websocket": URLRouter(
#             [path("graphql/", DjangoChannelsGraphQL(schema, debug=True))]
#         ),
#         "http": URLRouter(
#             [
#                 path("graphql/", DjangoChannelsGraphQL(schema, debug=True)),
#                 re_path(r"", AsgiHandler),
#             ]
#         ),
#     }
# )
