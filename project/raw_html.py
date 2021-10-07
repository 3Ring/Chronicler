from flask import url_for

class RawHTMLs():
    edit_button = '''
    <a data-editButtonAnchorId="{{ note.id }}" class="edit-note">
        <span data-flag="editButtons" data-id_editImage="{{ note.id }}" class='note_edit_button far fa-edit' src="/static/images/edit_button_image.png"></span>
    </a>
    '''



