import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import notes.schema


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()


class Query(UserQuery, MeQuery, notes.schema.Query, graphene.ObjectType):
    pass


class Mutation(AuthMutation, notes.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
