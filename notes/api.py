"""This module defines the /note routes."""

import datetime

from apiflask import APIBlueprint, input, output, doc

from notes.models import Note, InNoteSchema, OutNoteSchema

blueprint = APIBlueprint('notes', __name__)


@blueprint.post('/notes')
@input(InNoteSchema)
@output(OutNoteSchema,
        201,
        description="Newly created note",
        links={'getNoteByTitle':
                   {'operationId': 'getNote',
                    'parameters': {'title': '$response.body#/title'}
                    }
               }
        )
@doc(tag='Notes', operation_id='postNote')
def post_note(data: dict) -> Note:
    """Create a note

    Post a note with given title and text to the API."""
    note = Note(**data)
    note.added_timestamp = note.modified_timestamp = datetime.datetime.now()
    note.commit()
    return note


@blueprint.get('/notes/<string:title>')
@output(OutNoteSchema)
@doc(tag='Notes', operation_id='getNote')
def get_note(title: str) -> Note:
    """Get a note from the API."""
    note = Note.find_one({'title': title})
    return note


@blueprint.get('/notes')
@output(OutNoteSchema(many=True))
@doc(tag='Notes')
def get_notes() -> list[Note]:
    """Get all notes from the API."""
    return list(Note.find())
