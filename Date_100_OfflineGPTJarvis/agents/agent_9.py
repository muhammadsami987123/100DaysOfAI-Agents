# agent_9.py - MemoryNotesAgent

from data.database import Database
from tinydb import Query

class MemoryNotesAgent:
    def __init__(self, db_path='jarvis_db.json'):
        self.db = Database(db_path)
        self.notes_table = self.db.db.table('notes')

    def add_note(self, note_content):
        self.notes_table.insert({"content": note_content, "timestamp": self.db.get_timestamp()})
        return f"Note added: {note_content}"

    def list_notes(self):
        notes = self.notes_table.all()
        if not notes:
            return "You have no notes."
        
        note_list_str = "Your notes:\n"
        for i, note in enumerate(notes):
            note_list_str += f"{i+1}. {note['content']} (Added on: {note['timestamp']})\n"
        return note_list_str

    def find_note(self, keyword):
        Note = Query()
        results = self.notes_table.search(Note.content.search(keyword))
        if not results:
            return f"No notes found containing '{keyword}'."
        
        found_notes_str = f"Notes containing '{keyword}':\n"
        for i, note in enumerate(results):
            found_notes_str += f"{i+1}. {note['content']} (Added on: {note['timestamp']})\n"
        return found_notes_str

    def remove_note(self, index):
        notes = self.notes_table.all()
        if 0 <= index < len(notes):
            note_id = notes[index].doc_id
            removed_note_content = notes[index]['content']
            self.notes_table.remove(doc_ids=[note_id])
            return f"Removed note: {removed_note_content}"
        else:
            return "Invalid note index."
