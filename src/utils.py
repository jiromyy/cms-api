import base64
import tempfile
import os
import re
import subprocess
from dotenv import load_dotenv

load_dotenv(".env.development", override=True)

class ContentManagerUtilities:
    """
    This class contains utility methods for managing content.
    
    The methods in this class are used to:
    - Copy a file to a temporary directory
    - Delete a file from a temporary directory
    - Sanitize a filename
    
    The methods in this class are used by the IndexManager class.    
    """
    def _copy_temp(self, file, filename):
        """
        Copy the uploaded file to a temporary directory.
        
        Parameters:
        - file: the uploaded file
        
        Returns:
        - the path to the temporary file
        """
        # Create a temporary directory
        # self.tmp_dir = tempfile.mkdtemp()
        self.tmp_dir = tempfile.mkdtemp()
        bytes = base64.b64decode(file)

        # Create a file in the temporary directory with the same name as the original file
        self.tmp_path = os.path.join(self.tmp_dir, filename)
        with open(self.tmp_path, 'wb') as tmp:
            # Write the contents of the uploaded file to the temporary file
            tmp.write(bytes)

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
    
    def convert_docx_to_pdf(self, data, filename):
        """
        Convert a DOCX file to a PDF file using LibreOffice.
        
        Parameters:
        - data: the DOCX file

        Returns:
        - the PDF file
        """

        # Create a temporary directory
        input_path = self._copy_temp(data, filename)

        # Create a temporary directory for the output PDF
        output_dir = 'temps'
        print(f"Output directory: {output_dir}")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert the DOCX file to PDF using LibreOffice
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_path], check=True)

        # Define the output PDF path
        pdf_file_path = os.path.join(output_dir, os.path.basename(input_path).replace('.docx', '.pdf'))
        print(f"Expected PDF file path: {pdf_file_path}")

        # Check if the PDF file was created
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"PDF file was not created: {pdf_file_path}")
        else:
            print(f"PDF file created successfully: {pdf_file_path}")

        # Read the PDF file and encode it in Base64
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()
            encoded_pdf = base64.b64encode(pdf_bytes)

        # delete the temporary files
        # self._delete_temp(input_path)
        # self._delete_temp(pdf_file_path)

        return encoded_pdf