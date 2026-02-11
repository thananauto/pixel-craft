# Project Prompt Template: Production-Ready Web Application
## How to Use This Prompt for Building Similar Applications

> **Purpose:** This template provides a structured approach to building production-ready web applications with AI assistance. Based on building an Image Optimization Web App, it can be adapted for any full-stack web application project.

---

## 📋 Table of Contents

1. [Initial Project Prompt](#phase-1-initial-project-prompt)
2. [Architecture & Structure](#phase-2-architecture--structure)
3. [Core Implementation](#phase-3-core-implementation)
4. [Advanced Features](#phase-4-advanced-features)
5. [UI/UX Enhancement](#phase-5-uiux-enhancement)
6. [Bug Fixes & Optimization](#phase-6-bug-fixes--optimization)
7. [Documentation](#phase-7-documentation)
8. [Best Practices Reference](#best-practices-reference)

---

## Phase 1: Initial Project Prompt

### 🎯 Core Application Requirements

Use this template to start your project:

```markdown
I want to build a [APPLICATION TYPE] web application with the following requirements:

**Core Functionality:**
- [Primary feature 1 - e.g., "Upload and process images"]
- [Primary feature 2 - e.g., "Apply transformations with user controls"]
- [Primary feature 3 - e.g., "Download processed results"]

**Technical Stack:**
- Backend: [Framework - e.g., Flask/Django/FastAPI]
- Frontend: [Technology - e.g., Vanilla JS/React/Vue]
- Processing: [Library - e.g., Pillow/FFmpeg/pandas]
- Deployment: Docker + [Server - e.g., Gunicorn/uvicorn]

**File Support:**
- Accepted formats: [e.g., JPEG, PNG, WebP]
- Rejected formats: [e.g., SVG, GIF]
- Max file size: [e.g., 25MB]

**User Interface:**
- Modern drag-and-drop upload
- Before/after comparison view
- Real-time preview of results
- Progress indicators

**Security & Performance:**
- Rate limiting: [e.g., 30 requests/minute per IP]
- File validation: MIME type + extension checking
- Auto cleanup: Files deleted after [timeframe]
- Input sanitization

**Architecture Requirements:**
- Modular structure with separation of concerns
- Separate files for: routes, config, validation, processing
- Factory pattern for app initialization
- Blueprint/router-based routing

**Production Requirements:**
- Docker containerization
- Production WSGI/ASGI server
- Health check endpoint
- Structured logging
- Error handling
- Auto-restart on failure

Please start by:
1. Creating the project structure
2. Setting up configuration
3. Implementing core upload/download functionality
4. Adding basic file validation
```

### 🎨 Example: Image Optimizer Application

```markdown
I want to build an Image Optimization web application with the following requirements:

**Core Functionality:**
- Upload images via drag-and-drop
- Optimize JPEG, PNG, and WebP images
- Show side-by-side before/after comparison
- Download optimized results

**Technical Stack:**
- Backend: Flask 3.1+
- Frontend: Vanilla JavaScript (no frameworks)
- Image Processing: Pillow 11.0+
- Deployment: Docker + Gunicorn

**File Support:**
- Accepted: JPEG, PNG, WebP
- Rejected: SVG, GIF (security)
- Max size: 25MB

**User Interface:**
- Drag-and-drop upload zone
- Side-by-side image preview
- Progress bar during upload
- Real optimized image display

**Security & Performance:**
- Rate limiting: 30 requests/minute per IP
- MIME type validation with python-magic
- Secure filename handling
- Auto cleanup after download

**Architecture:**
- Modular structure: app.py, routes.py, config.py, validator.py, processor.py, cleanup.py
- Flask factory pattern with blueprints
- Background cleanup thread
- Separation of concerns

**Production:**
- Docker with multi-stage build
- Gunicorn with worker count = CPU * 2 + 1
- Health check endpoint at /health
- Structured logging to stdout
- Container auto-restart
```

---

## Phase 2: Architecture & Structure

### 📁 Project Structure Prompt

```markdown
Please create a modular project structure with the following components:

**Directory Layout:**
```
[project_name]
├── app.py                 # Application factory
├── routes.py             # API endpoints
├── config.py             # Configuration
├── validator.py          # Input validation
├── processor.py          # Core processing logic
├── cleanup.py            # Resource management
├── requirements.txt      # Dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Orchestration
├── gunicorn.conf.py      # Production config
├── .dockerignore         # Build optimization
├── .gitignore           # Version control
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Client logic
├── templates/
│   └── index.html       # Main UI
└── [temp_folder]/       # Auto-created temp storage
```

**Requirements:**
1. **app.py**: Flask factory pattern with rate limiter initialization
2. **routes.py**: Blueprint with all endpoints, error handling
3. **config.py**: Centralized settings, environment variable support
4. **validator.py**: File validation, MIME checking, secure filenames
5. **processor.py**: Core business logic with format-specific handling
6. **cleanup.py**: Background thread for temp file management

**Design Patterns:**
- Factory pattern for app creation
- Blueprint pattern for route organization
- Singleton pattern for cleanup manager
- Strategy pattern for format-specific processing

Please implement with:
- Comprehensive docstrings
- Type hints where applicable
- Error handling at all layers
- Logging for debugging
```

### 🔧 Configuration Template Prompt

```markdown
Create a comprehensive config.py with:

**Categories:**
1. **File Upload:**
   - Max file size with validation
   - Allowed/rejected extensions
   - MIME type whitelist
   - Temp folder configuration

2. **Processing:**
   - Quality ranges (min/max/default)
   - Transform bounds (e.g., resize limits)
   - Processing timeout
   - Preset configurations

3. **Security:**
   - Rate limiting rules
   - Secret key management
   - CORS settings (if needed)
   - Input sanitization rules

4. **Cleanup:**
   - File age threshold
   - Cleanup interval
   - Cleanup on response flag
   - Startup cleanup flag

5. **Production:**
   - Debug mode
   - Testing mode
   - Logging level
   - Environment detection

**Implementation:**
- Use os.environ.get() for sensitive values
- Provide sensible defaults
- Include validation for critical settings
- Add comments explaining each setting
- Organize in logical sections
```

---

## Phase 3: Core Implementation

### 🔨 Backend Implementation Prompt

```markdown
Implement the core backend functionality:

**Validation Layer (validator.py):**
```python
class FileValidator:
    @staticmethod
    def validate_upload(file, file_path):
        """
        Validate uploaded file with:
        - Extension check
        - MIME type verification (using python-magic)
        - File size validation
        - File existence check
        Return: {'valid': bool, 'error': str}
        """

    @staticmethod
    def get_safe_filename(original_filename):
        """
        Generate secure filename with:
        - werkzeug.secure_filename()
        - Timestamp for uniqueness
        - Extension preservation
        Return: safe_filename
        """
```

**Processing Layer (processor.py):**
```python
class [ProcessorName]:
    @staticmethod
    def process(input_path, output_path, options):
        """
        Process file with options:
        - Load and validate input
        - Apply transformations based on options
        - Format-specific optimization
        - Save output
        - Return results dict with metrics
        """

    @staticmethod
    def _process_[format_a](...):
        """Format-specific processing"""

    @staticmethod
    def _process_[format_b](...):
        """Format-specific processing"""
```

**Cleanup Layer (cleanup.py):**
```python
class FileCleanup:
    def __init__(self, app):
        """Initialize with Flask app, start background thread"""

    def cleanup_old_files(self):
        """Background cleanup of old files based on age"""

    def cleanup_specific_files(self, file_list):
        """Immediate cleanup of specific files"""

    def startup_cleanup(self):
        """Clean orphaned files on app start"""
```

**Route Layer (routes.py):**
```python
# Endpoints to implement:
GET  /                    # Main UI
POST /upload              # Upload and process
POST /reprocess           # Reprocess with new options
GET  /download/<file>     # Download with cleanup
GET  /preview/<file>      # Preview result
POST /cleanup-all         # Cleanup all files
GET  /health              # Health check
```

**Requirements:**
- Comprehensive error handling with try/except
- Logging for all operations
- Input validation at every layer
- Consistent return formats
- Resource cleanup in finally blocks
```

### 🎨 Frontend Implementation Prompt

```markdown
Implement the frontend with modern, clean UI:

**HTML Structure (templates/index.html):**
```html
<!-- Required sections: -->
1. Header with title and description
2. Upload section with drag-drop zone
3. Progress indicators (upload + processing)
4. Preview section (before/after comparison)
5. Options panel (collapsible/expandable)
6. Action buttons (download, reset, reprocess)
7. Error message display
8. Footer with info
```

**CSS Requirements (static/css/style.css):**
- Modern gradient background
- Card-based layout with shadows
- Custom slider styling
- Button hover effects
- Smooth animations (fade-in, slide-in)
- Responsive breakpoints:
  - Desktop: >1024px (multi-column)
  - Tablet: 768-1024px (2-column)
  - Mobile: <768px (single-column)
- Touch-friendly controls (44px minimum)

**JavaScript Functionality (static/js/app.js):**
```javascript
// Core functions to implement:

1. File Validation:
   - validateFile(file)
   - Check size, type, extension

2. Upload Handling:
   - handleFile(file)
   - uploadToServer(file, options)
   - showProgress()

3. UI State Management:
   - showPreview(beforeImage, afterImage)
   - updateStatistics(results)
   - toggleSections(section)

4. Event Handlers:
   - Drag and drop events
   - Form input changes
   - Button clicks
   - Slider updates

5. API Communication:
   - Using Fetch API
   - Proper error handling
   - Response parsing
   - State updates

6. Cleanup:
   - cleanupOnPageLoad()
   - cleanupOnUnload() using sendBeacon
```

**UX Patterns:**
- Show progress during operations
- Disable controls during processing
- Clear error messages with auto-hide
- Smooth transitions between states
- Loading indicators
- Visual feedback on all actions
```

---

## Phase 4: Advanced Features

### 🚀 Interactive Features Prompt

```markdown
Add interactive capabilities that enhance user experience:

**Feature 1: Reprocess Without Re-upload**

Implement a workflow where users can:
1. Upload file once (stored on server)
2. Adjust processing parameters
3. Click "Reprocess" to generate new output
4. Repeat steps 2-3 unlimited times
5. Download when satisfied

**Backend:**
- Keep original file on server after upload
- New endpoint: POST /reprocess
- Parameters: safe_filename + all processing options
- Regenerate output with new settings
- Return same response format as upload

**Frontend:**
- Store safe_filename after upload
- Enable settings controls after upload
- Add "Reprocess" button
- Show progress during reprocessing
- Update preview with new results
- Bandwidth savings: upload once, reprocess many times

**Feature 2: Advanced Processing Controls**

Add user-adjustable parameters:
- [Control 1]: Slider/dropdown/toggle with live preview
- [Control 2]: Range with value display and hints
- [Control 3]: Preset options (beginner-friendly)

**Implementation Pattern:**
```javascript
// Live value display
slider.addEventListener('input', (e) => {
    valueDisplay.textContent = formatValue(e.target.value);
    updatePreview();
});

// Preset application
presetSelect.addEventListener('change', (e) => {
    applyPreset(presets[e.target.value]);
});
```

**Feature 3: Format/Mode Conversion**

Allow output in different formats:
- Dropdown: "Keep original" or convert to X/Y/Z
- Handle transparency (e.g., RGBA → RGB with white bg)
- Update filename extension
- Preserve quality when possible

**Feature 4: Comparison Tools**

Interactive before/after comparison:
- Side-by-side layout (desktop)
- Stacked layout (mobile)
- Statistics display (size, dimensions, savings)
- Zoom functionality for detail inspection
```

### 🔍 Zoom/Magnifier Feature Prompt

```markdown
Implement click-to-zoom functionality:

**Requirements:**
1. Click on any image to open full-screen zoom modal
2. Interactive zoom controls (+/-/reset buttons)
3. Mouse wheel zoom (fine-grained control)
4. Click and drag to pan when zoomed
5. Pinch-to-zoom on mobile devices
6. ESC key and backdrop click to close
7. Touch gestures for mobile

**HTML Structure:**
```html
<!-- Add to images -->
<div class="clickable-image" data-image-type="before">
    <img id="beforeImage" src="...">
    <div class="zoom-hint">🔍 Click to zoom</div>
</div>

<!-- Zoom modal -->
<div id="zoomModal" class="zoom-modal">
    <button class="zoom-close">×</button>
    <div class="zoom-controls">
        <button class="zoom-in">+</button>
        <button class="zoom-reset">⟲</button>
        <button class="zoom-out">-</button>
    </div>
    <div class="zoom-container">
        <img id="zoomedImage" src="">
    </div>
    <div class="zoom-info">
        <span id="zoomLevel">100%</span> •
        Drag to pan • Scroll to zoom
    </div>
</div>
```

**CSS Requirements:**
```css
/* Full-screen modal with dark backdrop */
.zoom-modal {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.95);
    z-index: 10000;
}

/* Transform-based zoom (GPU accelerated) */
.zoom-container img {
    transform: scale(var(--zoom)) translate(var(--pan-x), var(--pan-y));
    transition: transform 0.2s ease;
}
```

**JavaScript Implementation:**
```javascript
// State management
let zoomScale = 1;
let panX = 0, panY = 0;
let isDragging = false;

// Zoom functions
function adjustZoom(delta) {
    zoomScale = Math.max(1, Math.min(5, zoomScale + delta));
    updateTransform();
}

// Pan functions
function handleMouseDown(e) {
    if (zoomScale > 1) {
        isDragging = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
    }
}

function handleMouseMove(e) {
    if (isDragging) {
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        updateTransform();
    }
}

// Touch support
function handlePinchZoom(e) {
    if (e.touches.length === 2) {
        const distance = calculateDistance(e.touches);
        const delta = (distance - lastDistance) / 100;
        adjustZoom(delta);
    }
}
```

**Zoom Capabilities:**
- Zoom range: 100% to 500%
- Button step: 25%
- Scroll step: 10%
- Smooth transitions
- Hardware acceleration
```

---

## Phase 5: UI/UX Enhancement

### 🎨 Responsive Design Prompt

```markdown
Implement responsive design for all devices:

**Breakpoint Strategy:**
```css
/* Desktop First Approach */
.container {
    max-width: 1400px;
    padding: 40px;
}

/* Tablet */
@media (max-width: 1024px) {
    .options-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Mobile */
@media (max-width: 768px) {
    .container { padding: 20px; }
    .options-grid {
        grid-template-columns: 1fr;
    }
    .comparison-container {
        grid-template-columns: 1fr; /* Stack images */
    }
    .action-buttons {
        flex-direction: column;
    }
    .action-buttons button {
        width: 100%;
    }
}

/* Small mobile */
@media (max-width: 480px) {
    /* Further optimizations */
}
```

**Grid Layout System:**
```css
/* Three-column layout (desktop) */
.options-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
}

/* Column cards */
.option-column {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.option-column h4 {
    color: var(--primary-color);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 10px;
}
```

**Touch Optimization:**
- Minimum touch target: 44px × 44px
- Adequate spacing between interactive elements
- Full-width buttons on mobile
- Disable hover effects on touch devices
- Use appropriate input types (number, range)

**Visual Enhancements:**
```markdown
1. **Icon-Enhanced Buttons:**
   - Add SVG icons to all buttons
   - Icon + text for clarity
   - Consistent icon style

2. **Progress Indicators:**
   - Animated progress bars
   - Clear status messages
   - Smooth color gradients
   - Show percentage when applicable

3. **Transitions:**
   - Smooth fade-in for new content
   - Slide animations for sections
   - Scale effects on hover
   - Loading spinners

4. **Color System:**
   - Primary: Main brand color
   - Success: Green for positive actions
   - Warning: Yellow/orange for caution
   - Error: Red for errors
   - Neutral: Gray for secondary actions

5. **State Management:**
   - Hide upload section after upload
   - Show/hide options panel
   - Enable/disable controls based on state
   - Loading states for async operations
```

---

## Phase 6: Bug Fixes & Optimization

### 🐛 Common Issues & Fixes Prompt

```markdown
Review and fix these common issues:

**Issue 1: Incomplete Data Cleanup**
**Problem:** [Data/metadata/cache not fully removed]
**Solution:**
- Identify all data storage locations
- Clear at multiple points (load, before save, after operations)
- Use complete wipe methods, not partial
- Verify with testing

**Example: Metadata Stripping**
```python
# Problem: Relying on implicit stripping
if not strip_metadata and exif_data:
    save_kwargs['exif'] = exif_data
# Metadata may still leak through img.info

# Solution: Explicit clearing
if strip_metadata:
    img.info = {}  # First clear after load

# ... processing ...

if strip_metadata:
    img.info = {}  # Second clear before save
```

**Issue 2: Memory Leaks**
**Problem:** Resources not properly released
**Solution:**
- Use context managers (with statements)
- Close file handles explicitly
- Clear large objects
- Reset state variables

```python
# Good pattern
with Image.open(input_path) as img:
    # Process image
    img.save(output_path)
# Image automatically closed

# After processing
del img  # Help garbage collector
```

**Issue 3: Race Conditions**
**Problem:** Concurrent access to shared resources
**Solution:**
- Use file locking if needed
- Atomic operations
- Unique filenames (timestamps)
- Proper cleanup order

**Issue 4: Error Handling Gaps**
**Problem:** Uncaught exceptions crash app
**Solution:**
```python
# Layer 1: Specific exceptions
try:
    result = process_file(file)
except FileNotFoundError:
    return error_response("File not found", 404)
except PermissionError:
    return error_response("Permission denied", 403)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return error_response("Processing failed", 500)
finally:
    cleanup_resources()
```

**Performance Optimizations:**
1. Use hardware acceleration (GPU) where possible
2. Cache expensive computations
3. Lazy load large resources
4. Optimize database queries (if applicable)
5. Compress responses (gzip)
6. Use CDN for static assets (production)
7. Implement pagination for large lists
8. Background processing for slow operations
```

---

## Phase 7: Documentation

### 📚 Documentation Prompt

```markdown
Create comprehensive documentation:

**1. README.md**
Structure:
- Project title and description
- Features list (organized by category)
- Requirements and dependencies
- Installation (local + Docker)
- Configuration guide
- API documentation
- Troubleshooting section
- License and support info

**2. SESSION_NOTES.md** (Development Log)
Include:
- Project overview
- Requirements (original + added)
- Implementation steps (chronological)
- Technical challenges and solutions
- Code statistics (files, lines, time)
- Feature verification checklist
- Key learnings
- Technology stack details

**3. INTERACTIVE_MODE.md** (Feature Guide)
Structure:
- Feature overview
- Step-by-step workflows
- Example scenarios
- Tips and tricks
- Benefits explanation
- FAQ section

**4. API_DOCUMENTATION.md**
Include:
- All endpoints with methods
- Request/response formats
- Authentication (if applicable)
- Rate limiting details
- Error codes and messages
- Example curl commands
- Code examples in multiple languages

**5. DEPLOYMENT.md**
Cover:
- Environment setup
- Configuration
- Docker deployment
- Cloud platform guides (AWS, GCP, Azure)
- Scaling considerations
- Monitoring setup
- Backup strategies

**Documentation Best Practices:**
- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Version your docs
- Keep updated with code changes
- Include troubleshooting
- Add table of contents for long docs
- Use proper markdown formatting
```

---

## Best Practices Reference

### 🏗️ Architecture Patterns

**Modular Design:**
```
✅ DO: Separate concerns into distinct modules
✅ DO: Use clear naming conventions
✅ DO: Keep functions focused and small
✅ DO: Use dependency injection
❌ DON'T: Put everything in one file
❌ DON'T: Create circular dependencies
```

**Configuration Management:**
```python
✅ DO: Centralize all config in config.py
✅ DO: Use environment variables for secrets
✅ DO: Provide sensible defaults
✅ DO: Validate critical settings
❌ DON'T: Hardcode configuration values
❌ DON'T: Store secrets in code
```

**Error Handling:**
```python
✅ DO: Use specific exception types
✅ DO: Log errors with context
✅ DO: Clean up resources in finally blocks
✅ DO: Return user-friendly error messages
❌ DON'T: Use bare except clauses
❌ DON'T: Expose internal errors to users
```

### 🎨 Frontend Best Practices

**State Management:**
```javascript
✅ DO: Keep state in variables
✅ DO: Update UI based on state
✅ DO: Validate state transitions
❌ DON'T: Query DOM for state
❌ DON'T: Allow invalid states
```

**Event Handling:**
```javascript
✅ DO: Use event delegation where appropriate
✅ DO: Debounce expensive operations
✅ DO: Clean up event listeners
❌ DON'T: Attach too many listeners
❌ DON'T: Ignore memory leaks
```

**API Communication:**
```javascript
✅ DO: Use Fetch API with proper error handling
✅ DO: Show loading states
✅ DO: Handle network failures gracefully
✅ DO: Implement request timeouts
❌ DON'T: Block UI during requests
❌ DON'T: Ignore error responses
```

### 🔒 Security Best Practices

**Input Validation:**
```python
✅ DO: Validate on both client and server
✅ DO: Use whitelist approach
✅ DO: Check file types with MIME detection
✅ DO: Sanitize filenames
✅ DO: Enforce size limits
❌ DON'T: Trust client-side validation alone
❌ DON'T: Use blacklist approach
```

**File Handling:**
```python
✅ DO: Use secure_filename()
✅ DO: Store files outside web root
✅ DO: Delete temporary files
✅ DO: Set proper permissions
❌ DON'T: Use user-provided filenames directly
❌ DON'T: Keep files indefinitely
```

**Rate Limiting:**
```python
✅ DO: Implement per-IP limits
✅ DO: Return proper 429 status
✅ DO: Include retry-after header
❌ DON'T: Allow unlimited requests
❌ DON'T: Use only client-side limiting
```

### 🚀 Performance Best Practices

**Backend:**
```python
✅ DO: Use async/await for I/O operations
✅ DO: Implement caching where appropriate
✅ DO: Optimize database queries
✅ DO: Use connection pooling
✅ DO: Profile and measure performance
❌ DON'T: Block on slow operations
❌ DON'T: Load entire files into memory
```

**Frontend:**
```javascript
✅ DO: Minimize DOM operations
✅ DO: Use CSS transforms for animations
✅ DO: Lazy load images and content
✅ DO: Debounce/throttle frequent events
❌ DON'T: Re-render entire page unnecessarily
❌ DON'T: Use synchronous blocking calls
```

### 📦 Deployment Best Practices

**Docker:**
```dockerfile
✅ DO: Use multi-stage builds
✅ DO: Use specific version tags
✅ DO: Run as non-root user
✅ DO: Minimize layer count
✅ DO: Use .dockerignore
❌ DON'T: Use :latest in production
❌ DON'T: Include dev dependencies
```

**Production:**
```bash
✅ DO: Use production WSGI server (Gunicorn/uvicorn)
✅ DO: Set up health checks
✅ DO: Implement logging
✅ DO: Use environment variables
✅ DO: Set up monitoring
❌ DON'T: Use Flask dev server
❌ DON'T: Enable debug mode
```

---

## Adaptation Guide

### 🔄 How to Adapt This Template

**For Different Application Types:**

1. **File Processing App** (Video, Audio, Documents):
   - Replace image processor with appropriate library
   - Adjust validation for new file types
   - Update UI for format-specific previews
   - Add format-specific options

2. **Data Processing App** (CSV, JSON, API):
   - Replace processor with data transformation logic
   - Add data validation layer
   - Implement streaming for large files
   - Add data preview/sampling

3. **API Integration App** (Third-party services):
   - Add API client module
   - Implement authentication
   - Add request queuing
   - Handle rate limits from external APIs

4. **Real-time App** (WebSocket/SSE):
   - Add WebSocket support (Flask-SocketIO)
   - Implement connection management
   - Add real-time status updates
   - Handle reconnection logic

5. **Multi-user App** (Authentication):
   - Add user management module
   - Implement session handling
   - Add per-user file isolation
   - Implement access control

### 📝 Customization Checklist

When adapting this template:

- [ ] Replace "image optimization" with your domain
- [ ] Update file type validations
- [ ] Modify processing logic for your use case
- [ ] Adjust UI components for your workflow
- [ ] Update configuration parameters
- [ ] Modify cleanup strategy if needed
- [ ] Adjust rate limits for your use case
- [ ] Update documentation with your specifics
- [ ] Add domain-specific features
- [ ] Update test scenarios
- [ ] Modify Docker configuration if needed
- [ ] Adjust resource limits (CPU, memory)

---

## Success Criteria

### ✅ Completion Checklist

**Phase 1: Core (v1.0)**
- [ ] Project structure created
- [ ] Basic upload/download working
- [ ] File validation implemented
- [ ] Error handling in place
- [ ] Docker working
- [ ] Basic documentation

**Phase 2: Advanced (v2.0)**
- [ ] Interactive features working
- [ ] Advanced processing options
- [ ] Re-process capability
- [ ] All features tested
- [ ] Enhanced documentation

**Phase 3: Polish (v2.1)**
- [ ] Responsive design complete
- [ ] Mobile-friendly UI
- [ ] Visual enhancements done
- [ ] Performance optimized
- [ ] Bug-free operation

**Phase 4: Production (v2.2)**
- [ ] All security measures in place
- [ ] Comprehensive testing done
- [ ] Production deployment tested
- [ ] Monitoring set up
- [ ] Documentation complete
- [ ] Ready for users

### 📊 Quality Metrics

**Code Quality:**
- Modular architecture (✓)
- Clear separation of concerns (✓)
- Comprehensive error handling (✓)
- Proper logging (✓)
- No code duplication (✓)

**User Experience:**
- Intuitive interface (✓)
- Responsive on all devices (✓)
- Clear feedback on actions (✓)
- Fast response times (✓)
- Helpful error messages (✓)

**Security:**
- Input validation (✓)
- Rate limiting (✓)
- Secure file handling (✓)
- No sensitive data exposure (✓)
- Proper authentication (if needed) (✓)

**Production Readiness:**
- Docker deployment (✓)
- Health checks (✓)
- Logging and monitoring (✓)
- Error recovery (✓)
- Documentation complete (✓)

---

## Appendix: Example Prompts

### Quick Start Prompt
```markdown
Using the project template, create a [TYPE] application with:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Stack: [Backend] + [Frontend] + [Processing Library]
Focus on modular architecture and production readiness.
```

### Enhancement Prompt
```markdown
Add [FEATURE] to the existing [APPLICATION]:
- Requirement: [Description]
- Integration: [How it fits]
- UI: [User interface changes]
- API: [Backend changes]

Maintain existing patterns and code quality.
```

### Bug Fix Prompt
```markdown
Fix issue in [MODULE] where [PROBLEM]:
- Current behavior: [Description]
- Expected behavior: [Description]
- Root cause: [If known]
- Solution: [Proposed fix]

Ensure fix doesn't break existing functionality.
```

### Documentation Prompt
```markdown
Create documentation for [FEATURE/MODULE]:
- Overview and purpose
- Usage instructions
- Code examples
- Configuration options
- Troubleshooting tips

Follow documentation patterns from README.md.
```

---

## 🎓 Learning Outcomes

By following this template, you'll build:
- Production-ready web applications
- Modular, maintainable codebases
- Responsive, modern UIs
- Secure, performant systems
- Comprehensive documentation
- Docker-ready deployments

**Key Skills Developed:**
- Full-stack web development
- Modular architecture design
- Security best practices
- Performance optimization
- Responsive UI design
- Docker containerization
- Production deployment
- Technical documentation

---

**Version:** 1.0
**Last Updated:** February 9, 2026
**Based On:** Image Optimization Web App (23 features, 5,635 lines of code)
**Success Rate:** 100% production-ready deployment

---

**Ready to build something amazing? Start with Phase 1 and iterate! 🚀**
