# pixel-craft

A production-ready Flask web application for optimizing JPEG, PNG, and WebP images with advanced controls and drag-and-drop upload functionality.

## Theme

pixel-craft features a clean, minimalist monochrome design with the following color palette:
- **Primary Black**: #1a1a1a - Headers and primary elements
- **Dark Grey**: #333333 - Primary buttons and interactive elements
- **Medium Grey**: #757575 - Secondary text and elements
- **Light Grey**: #e0e0e0 - Borders and dividers
- **Very Light Grey**: #f5f5f5 - Background panels
- **White**: #ffffff - Main surfaces

## Features

### Core Optimization
- **Modern Web UI**: Drag-and-drop interface with real-time before/after image preview
- **Advanced Image Optimization**: Compress images using Pillow with format-specific optimizations
- **Multiple Formats**: Support for JPEG, PNG, and WebP (SVG and GIF rejected)
- **Side-by-Side Comparison**: View original and optimized images simultaneously
- **Real "After" Image**: Shows the actual optimized image, not just a placeholder

### Advanced Controls
- **Quality Slider**: Adjust JPEG/WebP quality (1-95, default 85)
- **Resize by Percentage**: Scale images from 10% to 200% while preserving aspect ratio
- **Strip Metadata**: Toggle to remove or preserve EXIF data (default: strip)
- **Auto-Orient**: Automatically fix image rotation based on EXIF orientation data
- **Optimization Presets**:
  - **Speed**: Fast processing, larger files (Quality 90)
  - **Balanced**: Good balance of speed and quality (Quality 85, default)
  - **Max Quality**: Best quality, slower processing (Quality 95)
- **Live Settings Preview**: See your chosen options before processing

### Security & Performance
- **Rate Limiting**: 30 requests per minute per IP address
- **File Validation**: MIME type and extension checking with 25MB size limit
- **Immediate Cleanup**: Files deleted automatically after download (no retention)
- **Scheduled Cleanup**: Background cleanup of old temporary files
- **Production Ready**: Dockerized with Gunicorn for production deployment
- **OpenCV Ready**: OpenCV available for future feature enhancements

## Project Structure

```
image_optimization/
├── app.py                 # Flask app initialization
├── routes.py             # API endpoints and routes
├── config.py             # Configuration settings
├── validator.py          # File validation logic
├── cleanup.py            # Automatic file cleanup
├── image_processor.py    # Image optimization with Pillow
├── requirements.txt      # Python dependencies
├── gunicorn.conf.py      # Gunicorn production config
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker orchestration
├── static/
│   ├── css/style.css    # Styles
│   └── js/app.js        # Client-side logic
├── templates/
│   └── index.html       # Main UI template
└── uploads/             # Temporary file storage (auto-created)
```

## Requirements

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)

## Installation

### Option 1: Local Development

1. Clone the repository:
```bash
cd image_optimization
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python app.py
```

5. Open browser to `http://localhost:5000`

### Option 2: Docker Deployment (Production)

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. Access the app at `http://localhost:5000`

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the container:
```bash
docker-compose down
```

## API Endpoints

### `GET /`
Main web interface with drag-and-drop upload and advanced controls.

### `POST /upload`
Upload and optimize an image with custom options.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - `file`: Image file (required)
  - `quality`: Quality setting 1-95 (optional, default: 85)
  - `resize_percent`: Resize percentage 10-200 (optional, default: 100)
  - `strip_metadata`: Boolean (optional, default: true)
  - `auto_orient`: Boolean (optional, default: true)
  - `preset`: "speed", "balanced", or "max_quality" (optional, default: balanced)

**Response:**
```json
{
  "success": true,
  "original_filename": "photo.jpg",
  "safe_filename": "photo_1234567890.jpg",
  "original_size": 2048000,
  "optimized_size": 512000,
  "reduction_bytes": 1536000,
  "reduction_percent": 75.0,
  "format": "JPEG",
  "original_width": 1920,
  "original_height": 1080,
  "width": 1920,
  "height": 1080,
  "resized": false,
  "metadata_stripped": true,
  "auto_oriented": true,
  "preset": "balanced",
  "quality_used": 85,
  "download_url": "/download/photo_1234567890.jpg",
  "preview_url": "/preview/optimized/photo_1234567890.jpg"
}
```

### `GET /download/<filename>`
Download the optimized image. Files are automatically deleted after download.

### `GET /preview/<type>/<filename>`
Preview original or optimized image for display.
- `type`: "original" or "optimized"

### `GET /health`
Health check endpoint for Docker/monitoring.

## Configuration

Edit `config.py` to customize:

```python
# File upload settings
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB max file size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
REJECTED_EXTENSIONS = {'svg', 'gif'}

# Rate limiting
RATELIMIT_DEFAULT = "30 per minute"

# Cleanup settings
CLEANUP_AGE_SECONDS = 3600  # 1 hour
DELETE_AFTER_RESPONSE = True  # Delete files after download

# Quality settings
MIN_QUALITY = 1
MAX_QUALITY = 95
DEFAULT_QUALITY = 85

# Resize settings
MIN_RESIZE_PERCENT = 10
MAX_RESIZE_PERCENT = 200
DEFAULT_RESIZE_PERCENT = 100  # No resize

# Metadata & orientation
STRIP_METADATA_DEFAULT = True
AUTO_ORIENT_DEFAULT = True

# Optimization presets
PRESETS = {
    'speed': {
        'jpeg_quality': 90,
        'webp_quality': 90,
        'png_compress_level': 6,
        'webp_method': 4
    },
    'balanced': {
        'jpeg_quality': 85,
        'webp_quality': 85,
        'png_compress_level': 9,
        'webp_method': 6
    },
    'max_quality': {
        'jpeg_quality': 95,
        'webp_quality': 95,
        'png_compress_level': 9,
        'webp_method': 6
    }
}
```

## Image Optimization Settings

### JPEG
- Quality: Adjustable (1-95, default 85)
- Progressive encoding enabled
- Optimize flag enabled
- Auto-orient via EXIF
- Metadata stripping optional

### PNG
- Optimize enabled
- Compression level: 9 (maximum for balanced/max quality)
- Compression level: 6 (for speed preset)
- Metadata stripping optional

### WebP
- Quality: Adjustable (1-95, default 85)
- Method: 6 (best compression for balanced/max quality)
- Method: 4 (faster for speed preset)
- Metadata stripping optional

### Resize
- Percentage-based: 10% to 200%
- Preserves aspect ratio
- Uses LANCZOS resampling for quality

### Auto-Orient
- Automatically rotates images based on EXIF orientation
- Prevents sideways/upside-down images
- Applied before other processing

## Rate Limiting

The app implements rate limiting to prevent abuse:
- **Default**: 30 requests per minute per IP address
- Rate limit headers included in responses
- Configurable in `config.py`

## File Cleanup

The app implements two cleanup strategies:

### 1. Immediate Cleanup (Default)
- Files are deleted immediately after download
- No retention of processed images
- Configured via `DELETE_AFTER_RESPONSE = True`

### 2. Scheduled Cleanup (Background)
- Automatic cleanup removes old files
- **Default Age**: Files older than 1 hour are removed
- **Cleanup Interval**: Runs every 5 minutes
- **Startup Cleanup**: Orphaned files removed on app start
- Configurable in `config.py`

## Security Features

- MIME type validation (not just extension checking)
- Secure filename handling
- File size limits enforced
- SVG and GIF explicitly rejected
- Input sanitization
- Rate limiting per IP

## Production Deployment

The app is configured for production with:
- **Gunicorn**: Multi-worker WSGI server
- **Docker**: Containerized deployment
- **Health Checks**: Built-in health monitoring
- **Logging**: Structured logging to stdout
- **Auto-restart**: Container restarts on failure

### Environment Variables

Set in `docker-compose.yml` or `.env`:

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

## Future Enhancements

OpenCV is available but not currently used. Potential features:
- Advanced image filtering
- Face detection and blurring
- Watermarking
- Background removal
- Format conversion

## Troubleshooting

### Import Error: No module named 'magic'

Install system dependency:
```bash
# Ubuntu/Debian
sudo apt-get install libmagic1

# macOS
brew install libmagic
```

### Permission Denied on uploads/

Ensure uploads directory has correct permissions:
```bash
mkdir -p uploads
chmod 755 uploads
```

### Rate Limit Errors

Wait for rate limit to reset (1 minute) or adjust `RATELIMIT_DEFAULT` in config.

## License

MIT License - feel free to use for personal or commercial projects.

## Support

For issues or questions, please open an issue on the repository.
