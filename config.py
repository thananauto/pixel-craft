"""
Configuration settings for the Image Optimization Flask app.
"""
import os

class Config:
    """Base configuration class."""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB max file size

    # Allowed file extensions and MIME types
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    ALLOWED_MIME_TYPES = {
        'image/jpeg',
        'image/png',
        'image/webp'
    }

    # Rejected formats
    REJECTED_EXTENSIONS = {'svg', 'gif'}

    # Rate limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "30 per minute"
    RATELIMIT_HEADERS_ENABLED = True

    # File cleanup settings
    CLEANUP_AGE_SECONDS = 3600  # Remove files older than 1 hour
    CLEANUP_INTERVAL_SECONDS = 300  # Run cleanup every 5 minutes

    # Image optimization settings (defaults)
    JPEG_QUALITY = 85
    PNG_OPTIMIZE = True
    WEBP_QUALITY = 85

    # Quality slider bounds
    MIN_QUALITY = 1
    MAX_QUALITY = 95
    DEFAULT_QUALITY = 85

    # Resize bounds (percentage)
    MIN_RESIZE_PERCENT = 10
    MAX_RESIZE_PERCENT = 200
    DEFAULT_RESIZE_PERCENT = 100  # No resize

    # Metadata settings
    STRIP_METADATA_DEFAULT = True
    AUTO_ORIENT_DEFAULT = True

    # Sharpening settings
    SHARPEN_DEFAULT = 0  # 0 = no sharpen, 1-100 = sharpen intensity
    MIN_SHARPEN = 0
    MAX_SHARPEN = 100

    # Output format options
    OUTPUT_FORMATS = ['same', 'jpeg', 'png', 'webp']
    OUTPUT_FORMAT_DEFAULT = 'same'  # Keep original format

    # Optimization presets
    PRESETS = {
        'speed': {
            'jpeg_quality': 90,
            'webp_quality': 90,
            'png_compress_level': 6,
            'webp_method': 4,
            'description': 'Fast processing, larger files'
        },
        'balanced': {
            'jpeg_quality': 85,
            'webp_quality': 85,
            'png_compress_level': 9,
            'webp_method': 6,
            'description': 'Good balance of speed and quality'
        },
        'max_quality': {
            'jpeg_quality': 95,
            'webp_quality': 95,
            'png_compress_level': 9,
            'webp_method': 6,
            'description': 'Best quality, slower processing'
        }
    }
    DEFAULT_PRESET = 'balanced'

    # File retention
    DELETE_AFTER_RESPONSE = True  # Delete files immediately after downloading
    DELETE_AFTER_UPLOAD = False  # Keep files after upload to allow re-optimization

    # OpenCV availability flag (for future use)
    OPENCV_AVAILABLE = True

    @staticmethod
    def init_app(app):
        """Initialize app with configuration."""
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
