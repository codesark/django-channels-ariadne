from ariadne import (QueryType, gql, make_executable_schema,
                     snake_case_fallback_resolvers)

type_defs = gql("""
    type Query {
        hello: String!
    }
""")

query = QueryType()


@query.field("hello")
def resolve_hello(_, info):
    # request = info.context["request"]
    # user_agent = request.headers.get("user-agent", "guest")
    user = info.context["request"].user
    return f"Hello, {user}"


schema = make_executable_schema(
    type_defs,
    query,
    snake_case_fallback_resolvers
)
