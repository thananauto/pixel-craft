// Image Optimization App - Client-side JavaScript

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const errorMessage = document.getElementById('errorMessage');
const progressBar = document.getElementById('progressBar');
const reoptimizeProgress = document.getElementById('reoptimizeProgress');
const previewSection = document.getElementById('previewSection');
const optionsPanel = document.getElementById('optionsPanel');

const beforeImage = document.getElementById('beforeImage');
const afterImage = document.getElementById('afterImage');
const afterImageWrapper = document.getElementById('afterImageWrapper');
const beforeSize = document.getElementById('beforeSize');
const afterSize = document.getElementById('afterSize');
const savedSize = document.getElementById('savedSize');
const beforeDimensions = document.getElementById('beforeDimensions');
const beforeFormat = document.getElementById('beforeFormat');
const afterDimensions = document.getElementById('afterDimensions');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');
const reoptimizeBtn = document.getElementById('reoptimizeBtn');
const tipMessage = document.getElementById('tipMessage');

// Option elements
const presetSelect = document.getElementById('presetSelect');
const qualitySlider = document.getElementById('qualitySlider');
const qualityValue = document.getElementById('qualityValue');
const resizePercent = document.getElementById('resizePercent');
const resizeValue = document.getElementById('resizeValue');
const sharpenSlider = document.getElementById('sharpenSlider');
const sharpenValue = document.getElementById('sharpenValue');
const outputFormat = document.getElementById('outputFormat');
const stripMetadata = document.getElementById('stripMetadata');
const autoOrient = document.getElementById('autoOrient');

// Accordion elements
const accordionToggle = document.getElementById('accordionToggle');
const appliedSettingsAccordion = document.getElementById('appliedSettingsAccordion');

// Applied settings details (inside accordion)
const detailPreset = document.getElementById('detailPreset');
const detailQuality = document.getElementById('detailQuality');
const detailResize = document.getElementById('detailResize');
const detailSharpen = document.getElementById('detailSharpen');
const detailFormat = document.getElementById('detailFormat');
const detailMetadata = document.getElementById('detailMetadata');
const detailOrient = document.getElementById('detailOrient');

let currentDownloadUrl = null;
let currentSafeFilename = null;
let isOptimized = false;

// Zoom modal state
let zoomScale = 1;
let zoomPanX = 0;
let zoomPanY = 0;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;

// File size constraints
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp'];

// Cleanup all files on page load
function cleanupOnPageLoad() {
    fetch('/cleanup-all', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`Cleanup on load: ${data.count} files removed`);
        }
    })
    .catch(error => {
        console.warn('Cleanup on load failed:', error);
    });
}

// Cleanup all files when page is about to unload (refresh/close)
function cleanupOnUnload() {
    // Use sendBeacon for reliable cleanup even when page is closing
    const blob = new Blob([JSON.stringify({})], { type: 'application/json' });
    navigator.sendBeacon('/cleanup-all', blob);
}

// Initialize event listeners
function init() {
    // Cleanup files on page load
    cleanupOnPageLoad();

    // Cleanup files when page is refreshed or closed
    window.addEventListener('beforeunload', cleanupOnUnload);

    // Browse button click
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // Drop zone click
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        const file = e.dataTransfer.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Reset button
    resetBtn.addEventListener('click', () => {
        resetUI();
    });

    // Download button
    downloadBtn.addEventListener('click', () => {
        if (currentDownloadUrl) {
            window.location.href = currentDownloadUrl;
        }
    });

    // Re-optimize button
    reoptimizeBtn.addEventListener('click', () => {
        if (currentSafeFilename) {
            reoptimizeImage();
        }
    });

    // Accordion toggle
    if (accordionToggle) {
        accordionToggle.addEventListener('click', () => {
            appliedSettingsAccordion.classList.toggle('active');
        });
    }

    // Option change listeners for value display
    qualitySlider.addEventListener('input', updateQualityValue);
    resizePercent.addEventListener('input', updateResizeValue);
    sharpenSlider.addEventListener('input', updateSharpenValue);

    // Initialize zoom functionality
    initZoomFunctionality();
}

// Update quality value display
function updateQualityValue() {
    const value = qualitySlider.value;
    qualityValue.textContent = value;
}

// Update resize value display
function updateResizeValue() {
    const value = resizePercent.value;
    const status = value == 100 ? '(No resize)' : (value < 100 ? '(Smaller)' : '(Larger)');
    resizeValue.textContent = `${value}% ${status}`;
}

// Update sharpen value display
function updateSharpenValue() {
    const value = sharpenSlider.value;
    const status = value == 0 ? '(Off)' : (value < 50 ? '(Subtle)' : value < 80 ? '(Moderate)' : '(Strong)');
    sharpenValue.textContent = `${value} ${status}`;
}


// Get current optimization options
function getOptimizationOptions() {
    return {
        preset: presetSelect.value,
        quality: parseInt(qualitySlider.value),
        resize_percent: parseInt(resizePercent.value),
        sharpen: parseInt(sharpenSlider.value),
        output_format: outputFormat.value,
        strip_metadata: stripMetadata.checked,
        auto_orient: autoOrient.checked
    };
}

// Handle file upload
function handleFile(file) {
    // Hide error message
    hideError();

    // Validate file
    const validation = validateFile(file);
    if (!validation.valid) {
        showError(validation.error);
        return;
    }

    // Show preview of original image
    showOriginalPreview(file);

    // Upload and optimize
    uploadImage(file);
}

// Validate file
function validateFile(file) {
    // Check if file exists
    if (!file) {
        return { valid: false, error: 'No file selected' };
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        const sizeMB = (MAX_FILE_SIZE / (1024 * 1024)).toFixed(0);
        return { valid: false, error: `File size exceeds ${sizeMB}MB limit` };
    }

    // Check file type
    if (!ALLOWED_TYPES.includes(file.type)) {
        return { valid: false, error: 'Invalid file type. Please upload JPEG, PNG, or WebP only' };
    }

    // Check extension
    const extension = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(extension)) {
        return { valid: false, error: `${extension.toUpperCase()} files are not supported` };
    }

    return { valid: true };
}

// Show original image preview
function showOriginalPreview(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
        beforeImage.src = e.target.result;
        beforeSize.textContent = formatFileSize(file.size);

        // Detect format from filename
        const extension = file.name.split('.').pop().toUpperCase();
        beforeFormat.textContent = extension;

        // Get image dimensions
        const img = new Image();
        img.onload = () => {
            beforeDimensions.textContent = `${img.width} x ${img.height}`;
        };
        img.src = e.target.result;
    };

    reader.readAsDataURL(file);

    // Show preview section with placeholder
    previewSection.style.display = 'block';
    afterImageWrapper.querySelector('.placeholder').style.display = 'block';
    afterImage.style.display = 'none';
    downloadBtn.style.display = 'none';
    reoptimizeBtn.style.display = 'none';
    resetBtn.style.display = 'none';
    appliedSettingsAccordion.style.display = 'none';
    tipMessage.style.display = 'none';
    isOptimized = false;
}

// Upload image to server
function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    // Add optimization options
    const options = getOptimizationOptions();
    formData.append('quality', options.quality);
    formData.append('resize_percent', options.resize_percent);
    formData.append('sharpen', options.sharpen);
    formData.append('output_format', options.output_format);
    formData.append('strip_metadata', options.strip_metadata);
    formData.append('auto_orient', options.auto_orient);
    formData.append('preset', options.preset);

    // Show progress bar
    progressBar.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Upload failed');
            });
        }
        return response.json();
    })
    .then(data => {
        // Hide progress bar
        progressBar.style.display = 'none';

        // Hide upload section and show options
        uploadSection.classList.add('hidden');
        optionsPanel.style.display = 'block';

        // Save the safe filename for re-optimization
        currentSafeFilename = data.safe_filename;
        isOptimized = true;

        // Show optimized image
        showOptimizedImage(data);

        // Show tip message
        tipMessage.style.display = 'block';
    })
    .catch(error => {
        progressBar.style.display = 'none';
        showError(error.message);
        // Reset after pane
        afterImageWrapper.querySelector('.placeholder').style.display = 'block';
        afterImage.style.display = 'none';
    });
}

// Re-optimize existing image with new settings
function reoptimizeImage() {
    if (!currentSafeFilename) {
        showError('No image to re-optimize. Please upload an image first.');
        return;
    }

    const formData = new FormData();
    formData.append('safe_filename', currentSafeFilename);

    // Add current optimization options
    const options = getOptimizationOptions();
    formData.append('quality', options.quality);
    formData.append('resize_percent', options.resize_percent);
    formData.append('sharpen', options.sharpen);
    formData.append('output_format', options.output_format);
    formData.append('strip_metadata', options.strip_metadata);
    formData.append('auto_orient', options.auto_orient);
    formData.append('preset', options.preset);

    // Show progress bar for re-optimization
    if (reoptimizeProgress) {
        reoptimizeProgress.style.display = 'block';
    }

    // Show placeholder while re-optimizing
    afterImageWrapper.querySelector('.placeholder').innerHTML = '<p>Re-optimizing...</p>';
    afterImageWrapper.querySelector('.placeholder').style.display = 'block';
    afterImage.style.display = 'none';

    fetch('/reoptimize', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Re-optimization failed');
            });
        }
        return response.json();
    })
    .then(data => {
        // Hide progress bar
        if (reoptimizeProgress) {
            reoptimizeProgress.style.display = 'none';
        }

        // Show updated optimized image
        showOptimizedImage(data);

        // Reset placeholder text
        afterImageWrapper.querySelector('.placeholder').innerHTML = '<p>Processing...</p>';
    })
    .catch(error => {
        if (reoptimizeProgress) {
            reoptimizeProgress.style.display = 'none';
        }
        showError(error.message);
        // Reset placeholder
        afterImageWrapper.querySelector('.placeholder').innerHTML = '<p>Processing...</p>';
        afterImageWrapper.querySelector('.placeholder').style.display = 'block';
        afterImage.style.display = 'none';
    });
}

// Show optimized image
function showOptimizedImage(data) {
    // Update after image - show the real optimized image
    afterImage.src = data.preview_url + '?t=' + new Date().getTime(); // Add timestamp to prevent caching
    afterImage.onload = () => {
        afterImage.style.display = 'block';
        afterImageWrapper.querySelector('.placeholder').style.display = 'none';
    };

    // Update stats
    afterSize.textContent = formatFileSize(data.optimized_size);
    afterDimensions.textContent = `${data.width} x ${data.height}`;

    // Calculate and show savings
    const savingsText = data.reduction_percent >= 0
        ? `${data.reduction_percent}% (${formatFileSize(data.reduction_bytes)})`
        : 'File increased';
    savedSize.textContent = savingsText;
    savedSize.className = data.reduction_percent >= 0 ? 'highlight' : 'highlight-warning';

    // Show applied settings accordion
    appliedSettingsAccordion.style.display = 'block';
    detailPreset.textContent = capitalizeFirst(data.preset.replace('_', ' '));
    detailQuality.textContent = data.quality_used ? data.quality_used : 'N/A (PNG)';
    detailResize.textContent = data.resized
        ? `Yes (${data.original_width}x${data.original_height} → ${data.width}x${data.height})`
        : 'No';
    detailSharpen.textContent = data.sharpened ? `Yes (${data.sharpen_amount})` : 'No';
    detailFormat.textContent = data.format_converted
        ? `${data.format} → ${data.output_format}`
        : data.output_format;
    detailMetadata.textContent = data.metadata_stripped ? 'Stripped' : 'Preserved';
    detailOrient.textContent = data.auto_oriented ? 'Yes' : 'No';

    // Store download URL
    currentDownloadUrl = data.download_url;

    // Show buttons
    downloadBtn.style.display = 'inline-flex';
    reoptimizeBtn.style.display = 'inline-flex';
    resetBtn.style.display = 'inline-flex';
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Capitalize first letter
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Reset UI
function resetUI() {
    // Show upload section again
    uploadSection.classList.remove('hidden');
    optionsPanel.style.display = 'none';

    previewSection.style.display = 'none';
    progressBar.style.display = 'none';
    if (reoptimizeProgress) {
        reoptimizeProgress.style.display = 'none';
    }
    appliedSettingsAccordion.style.display = 'none';
    appliedSettingsAccordion.classList.remove('active');
    tipMessage.style.display = 'none';
    hideError();
    fileInput.value = '';
    currentDownloadUrl = null;
    currentSafeFilename = null;
    isOptimized = false;

    // Reset images
    beforeImage.src = '';
    afterImage.src = '';
    beforeSize.textContent = '-';
    afterSize.textContent = '-';
    savedSize.textContent = '-';
    beforeDimensions.textContent = '-';
    afterDimensions.textContent = '-';
    beforeFormat.textContent = '-';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize app on page load
document.addEventListener('DOMContentLoaded', init);

// ===== ZOOM FUNCTIONALITY =====

function initZoomFunctionality() {
    const modal = document.getElementById('imageZoomModal');
    const zoomedImage = document.getElementById('zoomedImage');
    const zoomContainer = document.getElementById('zoomImageContainer');
    const closeBtn = document.getElementById('zoomCloseBtn');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomResetBtn = document.getElementById('zoomResetBtn');
    const zoomLevelDisplay = document.getElementById('zoomLevel');
    const zoomImageTypeDisplay = document.getElementById('zoomImageType');

    // Add click handlers to images
    const beforeImageWrapper = document.querySelector('[data-image-type="before"]');
    const afterImageWrapper = document.querySelector('[data-image-type="after"]');

    beforeImageWrapper.addEventListener('click', function() {
        const img = document.getElementById('beforeImage');
        if (img.src && img.src !== window.location.href) {
            openZoomModal(img.src, 'Before (Original)');
        }
    });

    afterImageWrapper.addEventListener('click', function() {
        const img = document.getElementById('afterImage');
        if (img.style.display !== 'none' && img.src && img.src !== window.location.href) {
            openZoomModal(img.src, 'After (Optimized)');
        }
    });

    // Close modal
    closeBtn.addEventListener('click', closeZoomModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeZoomModal();
        }
    });

    // Escape key to close
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeZoomModal();
        }
    });

    // Zoom controls
    zoomInBtn.addEventListener('click', () => adjustZoom(0.25));
    zoomOutBtn.addEventListener('click', () => adjustZoom(-0.25));
    zoomResetBtn.addEventListener('click', resetZoom);

    // Mouse wheel zoom
    zoomContainer.addEventListener('wheel', function(e) {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.1 : 0.1;
        adjustZoom(delta);
    });

    // Touch zoom (pinch)
    let touchDistance = 0;
    zoomContainer.addEventListener('touchstart', function(e) {
        if (e.touches.length === 2) {
            touchDistance = Math.hypot(
                e.touches[0].pageX - e.touches[1].pageX,
                e.touches[0].pageY - e.touches[1].pageY
            );
        }
    });

    zoomContainer.addEventListener('touchmove', function(e) {
        if (e.touches.length === 2) {
            e.preventDefault();
            const newDistance = Math.hypot(
                e.touches[0].pageX - e.touches[1].pageX,
                e.touches[0].pageY - e.touches[1].pageY
            );
            const delta = (newDistance - touchDistance) / 100;
            adjustZoom(delta);
            touchDistance = newDistance;
        }
    });

    // Pan functionality - Mouse
    zoomContainer.addEventListener('mousedown', function(e) {
        if (zoomScale > 1) {
            isDragging = true;
            dragStartX = e.clientX - zoomPanX;
            dragStartY = e.clientY - zoomPanY;
            zoomContainer.classList.add('dragging');
        }
    });

    document.addEventListener('mousemove', function(e) {
        if (isDragging) {
            zoomPanX = e.clientX - dragStartX;
            zoomPanY = e.clientY - dragStartY;
            updateZoomTransform();
        }
    });

    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            zoomContainer.classList.remove('dragging');
        }
    });

    // Pan functionality - Touch
    let touchStartX = 0;
    let touchStartY = 0;
    zoomContainer.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1 && zoomScale > 1) {
            touchStartX = e.touches[0].clientX - zoomPanX;
            touchStartY = e.touches[0].clientY - zoomPanY;
        }
    });

    zoomContainer.addEventListener('touchmove', function(e) {
        if (e.touches.length === 1 && zoomScale > 1) {
            e.preventDefault();
            zoomPanX = e.touches[0].clientX - touchStartX;
            zoomPanY = e.touches[0].clientY - touchStartY;
            updateZoomTransform();
        }
    });

    function openZoomModal(imageSrc, imageType) {
        zoomedImage.src = imageSrc;
        zoomImageTypeDisplay.textContent = imageType;
        modal.style.display = 'flex';
        resetZoom();
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    function closeZoomModal() {
        modal.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
        resetZoom();
    }

    function adjustZoom(delta) {
        zoomScale = Math.max(1, Math.min(5, zoomScale + delta));
        updateZoomTransform();
        updateZoomLevelDisplay();
    }

    function resetZoom() {
        zoomScale = 1;
        zoomPanX = 0;
        zoomPanY = 0;
        updateZoomTransform();
        updateZoomLevelDisplay();
    }

    function updateZoomTransform() {
        zoomedImage.style.transform = `scale(${zoomScale}) translate(${zoomPanX / zoomScale}px, ${zoomPanY / zoomScale}px)`;
    }

    function updateZoomLevelDisplay() {
        zoomLevelDisplay.textContent = Math.round(zoomScale * 100) + '%';
    }
}
