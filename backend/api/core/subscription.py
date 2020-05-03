from ariadne import gql, SubscriptionType

subscription = SubscriptionType()

subscription_typedef = gql("""
    type Subscription{
        _empty: String
    }
""")
