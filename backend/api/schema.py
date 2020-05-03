from ariadne import make_executable_schema, snake_case_fallback_resolvers

from .account.schema import account_typedefs
from .core import (mutation, mutation_typedef, query, query_typedef,
                   subscription, subscription_typedef)
from .scalars import scalars

base_typedef = "\n\n".join([
    query_typedef,
    mutation_typedef,
    subscription_typedef
])

schema = make_executable_schema(
    "\n\n".join([
        scalars,
        base_typedef,
        account_typedefs,
    ]),
    query,
    mutation,
    subscription,
    snake_case_fallback_resolvers
)
