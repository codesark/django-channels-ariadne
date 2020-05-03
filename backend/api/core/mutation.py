from ariadne import gql, MutationType

mutation = MutationType()

mutation_typedef = gql("""
    type Mutation{
        _empty: String
    }
""")
