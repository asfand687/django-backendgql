import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from .models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        filter_fields = ["id", "body", "created", "owner"]
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    all_notes = DjangoFilterConnectionField(NoteType)
    note = graphene.relay.Node.Field(NoteType)


class CreateNote(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteType)

    class Input:
        body = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        if(info.context.user.pk is not None):
            note = Note(input.get('body'),  owner_id=info.context.user.pk)
            note.save()
            return CreateNote(
                note
            )
        else:
            raise GraphQLError('You must be logged to create the note!')


class UpdateNote(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteType)

    class Input:
        id = graphene.ID()
        body = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        note = Note.objects.get(id=input.get('id'))
        note.body = input.get('body')
        note.save()

        return UpdateNote(
            note
        )


class DeleteNote(graphene.relay.ClientIDMutation):
    msg = graphene.String()

    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        note = Note.objects.get(id=input.get('id')) or None
        if(note is not None):
            note.delete()
            return DeleteNote(
                msg="note deleted successfull"
            )
        else:
            raise GraphQLError('Note not found')


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()
