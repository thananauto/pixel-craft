"""
Cleanup module for temporary uploaded files.
Removes old files from the upload directory.
"""
import os
import time
from flask import current_app


class FileCleanup:
    """File cleanup manager for temporary uploads."""

    def __init__(self, app=None):
        """Initialize cleanup manager."""
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize cleanup with Flask app."""
        self.app = app

        # Clean up orphaned files on startup
        with app.app_context():
            self.cleanup_old_files()

    def cleanup_old_files(self):
        """Remove files older than configured age from upload folder."""
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            max_age = current_app.config['CLEANUP_AGE_SECONDS']
            current_time = time.time()

            if not os.path.exists(upload_folder):
                return

            removed_count = 0
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)

                # Skip directories
                if os.path.isdir(file_path):
                    continue

                # Check file age
                try:
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age:
                        os.remove(file_path)
                        removed_count += 1
                        current_app.logger.info(f"Cleaned up old file: {filename}")
                except Exception as e:
                    current_app.logger.error(f"Error removing file {filename}: {e}")

            if removed_count > 0:
                current_app.logger.info(f"Cleanup completed: {removed_count} files removed")

        except Exception as e:
            current_app.logger.error(f"Error during cleanup: {e}")

    def cleanup_specific_files(self, file_paths):
        """
        Remove specific files immediately.

        Args:
            file_paths (list): List of file paths to remove
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    current_app.logger.info(f"Removed file: {file_path}")
            except Exception as e:
                current_app.logger.error(f"Error removing file {file_path}: {e}")
