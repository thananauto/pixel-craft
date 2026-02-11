"""
File validation module for image uploads.
Validates file types, extensions, and MIME types.
"""
import os
import magic
from werkzeug.utils import secure_filename
from flask import current_app


class FileValidator:
    """Validator class for uploaded files."""

    @staticmethod
    def allowed_file(filename):
        """
        Check if filename has an allowed extension.

        Args:
            filename (str): Name of the uploaded file

        Returns:
            bool: True if extension is allowed, False otherwise
        """
        if not filename or '.' not in filename:
            return False

        extension = filename.rsplit('.', 1)[1].lower()
        allowed = extension in current_app.config['ALLOWED_EXTENSIONS']
        rejected = extension in current_app.config['REJECTED_EXTENSIONS']

        return allowed and not rejected

    @staticmethod
    def validate_mime_type(file_path):
        """
        Validate the MIME type of an uploaded file using python-magic.

        Args:
            file_path (str): Path to the uploaded file

        Returns:
            tuple: (bool, str) - (is_valid, mime_type)
        """
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)

            is_valid = mime_type in current_app.config['ALLOWED_MIME_TYPES']
            return is_valid, mime_type
        except Exception as e:
            current_app.logger.error(f"Error detecting MIME type: {e}")
            return False, "unknown"

    @staticmethod
    def validate_file_size(file_path):
        """
        Validate file size is within limits.

        Args:
            file_path (str): Path to the uploaded file

        Returns:
            tuple: (bool, int) - (is_valid, file_size_bytes)
        """
        try:
            file_size = os.path.getsize(file_path)
            max_size = current_app.config['MAX_CONTENT_LENGTH']
            return file_size <= max_size, file_size
        except Exception as e:
            current_app.logger.error(f"Error checking file size: {e}")
            return False, 0

    @staticmethod
    def get_safe_filename(filename):
        """
        Generate a safe filename with timestamp to prevent conflicts.

        Args:
            filename (str): Original filename

        Returns:
            str: Safe filename with timestamp
        """
        import time
        safe_name = secure_filename(filename)
        timestamp = str(int(time.time() * 1000))
        name, ext = os.path.splitext(safe_name)
        return f"{name}_{timestamp}{ext}"

    @staticmethod
    def validate_upload(file, file_path):
        """
        Comprehensive validation of uploaded file.

        Args:
            file: FileStorage object
            file_path (str): Path where file was saved

        Returns:
            dict: Validation result with 'valid' boolean and 'error' message
        """
        # Check if file has a valid extension
        if not FileValidator.allowed_file(file.filename):
            extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown'
            if extension in current_app.config['REJECTED_EXTENSIONS']:
                return {
                    'valid': False,
                    'error': f'{extension.upper()} files are not supported. Please upload JPEG, PNG, or WebP only.'
                }
            return {
                'valid': False,
                'error': 'Invalid file type. Please upload JPEG, PNG, or WebP images only.'
            }

        # Validate MIME type
        is_valid_mime, mime_type = FileValidator.validate_mime_type(file_path)
        if not is_valid_mime:
            return {
                'valid': False,
                'error': f'Invalid file format detected (MIME: {mime_type}). Please upload a valid image.'
            }

        # Validate file size
        is_valid_size, file_size = FileValidator.validate_file_size(file_path)
        if not is_valid_size:
            max_mb = current_app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
            return {
                'valid': False,
                'error': f'File size exceeds maximum allowed size of {max_mb}MB.'
            }

        return {
            'valid': True,
            'mime_type': mime_type,
            'file_size': file_size
        }
