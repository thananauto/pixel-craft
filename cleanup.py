"""
Automatic cleanup module for temporary uploaded files.
Removes old files from the upload directory.
"""
import os
import time
import threading
from flask import current_app


class FileCleanup:
    """File cleanup manager for temporary uploads."""

    def __init__(self, app=None):
        """Initialize cleanup manager."""
        self.app = app
        self._cleanup_thread = None
        self._stop_event = threading.Event()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize cleanup with Flask app."""
        self.app = app

        # Clean up orphaned files on startup
        with app.app_context():
            self.cleanup_old_files()

        # Start background cleanup thread
        self.start_background_cleanup()

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

    def _background_cleanup_task(self):
        """Background task that runs periodic cleanup."""
        interval = self.app.config['CLEANUP_INTERVAL_SECONDS']

        while not self._stop_event.is_set():
            # Wait for the interval or until stop event is set
            if self._stop_event.wait(timeout=interval):
                break

            # Run cleanup within app context
            with self.app.app_context():
                self.cleanup_old_files()

    def start_background_cleanup(self):
        """Start the background cleanup thread."""
        if self._cleanup_thread is None or not self._cleanup_thread.is_alive():
            self._stop_event.clear()
            self._cleanup_thread = threading.Thread(
                target=self._background_cleanup_task,
                daemon=True,
                name="FileCleanupThread"
            )
            self._cleanup_thread.start()
            self.app.logger.info("Background cleanup thread started")

    def stop_background_cleanup(self):
        """Stop the background cleanup thread."""
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._stop_event.set()
            self._cleanup_thread.join(timeout=5)
            self.app.logger.info("Background cleanup thread stopped")
