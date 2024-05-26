import tempfile
import os
import re
from dotenv import load_dotenv

load_dotenv()

class ContentManagerUtilities:
    """
    This class contains utility methods for managing content.
    
    The methods in this class are used to:
    - Copy a file to a temporary directory
    - Delete a file from a temporary directory
    - Sanitize a filename
    
    The methods in this class are used by the IndexManager class.    
    """
    def _copy_temp(self, file):
        """
        Copy the uploaded file to a temporary directory.
        
        Parameters:
        - file: the uploaded file
        
        Returns:
        - the path to the temporary file
        """
        # Get the original file name
        self.original_file_name = file.name

        # Create a temporary directory
        self.tmp_dir = tempfile.mkdtemp()

        # Create a file in the temporary directory with the same name as the original file
        self.tmp_path = os.path.join(self.tmp_dir, self.original_file_name)
        with open(self.tmp_path, 'wb') as tmp:
            # Write the contents of the uploaded file to the temporary file
            tmp.write(file.read())

        return self.tmp_path

    def _delete_temp(self, path):
        """
        Delete a file from a temporary directory.
        
        Parameters:
        - path: the path to the file
        
        Returns:
        - None
        """
        os.unlink(path)

    def sanitize_filename(self, filename):
        """
        Sanitize a filename.
        
        Parameters:
        - filename: the filename to sanitize
        
        Returns:
        - the sanitized filename
        """
        # Convert to lowercase
        self.filename = filename.lower()

        # Remove invalid characters
        self.filename = re.sub(r'[^a-z0-9]', '-', self.filename)

        # Replace multiple consecutive hyphens with a single hyphen
        self.filename = re.sub(r'-+', '-', self.filename)

        # Remove leading and trailing hyphens
        self.filename = self.filename.strip('-')

        # Truncate to 63 characters
        self.filename = self.filename[:63]
        print(self.filename)

        return self.filename