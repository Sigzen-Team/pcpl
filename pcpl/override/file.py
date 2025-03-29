import frappe
from frappe.core.doctype.file.file import File

# Create a custom class to override the File Doctype behavior
class CustomFile(File):
    
    def before_insert(self):
        # Call the parent before_insert method
        super().before_insert()

        # Now modify the save_file call to add ignore_existing_file_check=True
        if not self.is_folder and not self.is_remote_file:
            self.save_file(content=self.get_content(), ignore_existing_file_check=True)
            self.flags.new_file = True
            frappe.db.after_rollback.add(self.on_rollback)

