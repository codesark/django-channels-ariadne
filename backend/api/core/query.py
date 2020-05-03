from ariadne import gql, QueryType

query = QueryType()

query_typedef = gql("""
    type Query{
        _empty: String
    }
""")
