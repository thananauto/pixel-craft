"""
Flask routes for the image optimization app.
"""
import os
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from validator import FileValidator
from image_processor import ImageOptimizer
from cleanup import FileCleanup

# Create Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@main_bp.route('/reoptimize', methods=['POST'])
def reoptimize_image():
    """
    Re-optimize an already uploaded image with new settings.

    Returns:
        JSON response with new optimization results
    """
    try:
        # Get the safe filename from request
        safe_filename = request.form.get('safe_filename')
        if not safe_filename:
            return jsonify({'error': 'No filename provided'}), 400

        upload_folder = current_app.config['UPLOAD_FOLDER']
        input_path = os.path.join(upload_folder, f"original_{safe_filename}")

        # Check if original file exists
        if not os.path.exists(input_path):
            return jsonify({'error': 'Original file not found. Please re-upload.'}), 404

        # Parse optimization options
        try:
            quality = int(request.form.get('quality', current_app.config['DEFAULT_QUALITY']))
            quality = max(current_app.config['MIN_QUALITY'], min(quality, current_app.config['MAX_QUALITY']))

            resize_percent = int(request.form.get('resize_percent', current_app.config['DEFAULT_RESIZE_PERCENT']))
            resize_percent = max(
                current_app.config['MIN_RESIZE_PERCENT'],
                min(resize_percent, current_app.config['MAX_RESIZE_PERCENT'])
            )

            sharpen = int(request.form.get('sharpen', current_app.config['SHARPEN_DEFAULT']))
            sharpen = max(current_app.config['MIN_SHARPEN'], min(sharpen, current_app.config['MAX_SHARPEN']))

            strip_metadata = request.form.get('strip_metadata', 'true').lower() == 'true'
            auto_orient = request.form.get('auto_orient', 'true').lower() == 'true'
            preset = request.form.get('preset', current_app.config['DEFAULT_PRESET'])
            output_format = request.form.get('output_format', current_app.config['OUTPUT_FORMAT_DEFAULT'])

            if preset not in current_app.config['PRESETS']:
                preset = current_app.config['DEFAULT_PRESET']

            if output_format not in current_app.config['OUTPUT_FORMATS']:
                output_format = current_app.config['OUTPUT_FORMAT_DEFAULT']

        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid options: {str(e)}'}), 400

        output_path = os.path.join(upload_folder, f"optimized_{safe_filename}")

        # Prepare optimization options
        options = {
            'quality': quality,
            'resize_percent': resize_percent,
            'strip_metadata': strip_metadata,
            'auto_orient': auto_orient,
            'preset': preset,
            'sharpen': sharpen,
            'output_format': output_format
        }

        # Update output path if format changed
        if output_format != 'same':
            base_name = os.path.splitext(safe_filename)[0]
            new_filename = f"{base_name}.{output_format}"
            output_path = os.path.join(upload_folder, f"optimized_{new_filename}")

        # Re-optimize the image
        optimization_result = ImageOptimizer.optimize_image(input_path, output_path, options)

        if not optimization_result['success']:
            return jsonify({'error': f"Optimization failed: {optimization_result.get('error', 'Unknown error')}"}), 500

        # Update safe filename if format changed
        final_filename = safe_filename
        if optimization_result.get('format_converted'):
            base_name = os.path.splitext(safe_filename)[0]
            final_filename = f"{base_name}.{output_format}"

        # Prepare response
        response_data = {
            'success': True,
            'safe_filename': final_filename,
            'original_size': optimization_result['original_size'],
            'optimized_size': optimization_result['optimized_size'],
            'reduction_bytes': optimization_result['reduction_bytes'],
            'reduction_percent': optimization_result['reduction_percent'],
            'format': optimization_result['format'],
            'output_format': optimization_result['output_format'],
            'format_converted': optimization_result['format_converted'],
            'original_width': optimization_result['original_width'],
            'original_height': optimization_result['original_height'],
            'width': optimization_result['width'],
            'height': optimization_result['height'],
            'resized': optimization_result['resized'],
            'metadata_stripped': optimization_result['metadata_stripped'],
            'auto_oriented': optimization_result['auto_oriented'],
            'preset': optimization_result['preset'],
            'quality_used': optimization_result['quality_used'],
            'sharpened': optimization_result['sharpened'],
            'sharpen_amount': optimization_result['sharpen_amount'],
            'download_url': f'/download/{final_filename}',
            'preview_url': f'/preview/optimized/{final_filename}'
        }

        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error re-optimizing image: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@main_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Handle image upload and optimization with options.

    Returns:
        JSON response with optimization results
    """
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Parse optimization options from form data
    try:
        quality = int(request.form.get('quality', current_app.config['DEFAULT_QUALITY']))
        quality = max(current_app.config['MIN_QUALITY'], min(quality, current_app.config['MAX_QUALITY']))

        resize_percent = int(request.form.get('resize_percent', current_app.config['DEFAULT_RESIZE_PERCENT']))
        resize_percent = max(
            current_app.config['MIN_RESIZE_PERCENT'],
            min(resize_percent, current_app.config['MAX_RESIZE_PERCENT'])
        )

        sharpen = int(request.form.get('sharpen', current_app.config['SHARPEN_DEFAULT']))
        sharpen = max(current_app.config['MIN_SHARPEN'], min(sharpen, current_app.config['MAX_SHARPEN']))

        strip_metadata = request.form.get('strip_metadata', 'true').lower() == 'true'
        auto_orient = request.form.get('auto_orient', 'true').lower() == 'true'
        preset = request.form.get('preset', current_app.config['DEFAULT_PRESET'])
        output_format = request.form.get('output_format', current_app.config['OUTPUT_FORMAT_DEFAULT'])

        # Validate preset
        if preset not in current_app.config['PRESETS']:
            preset = current_app.config['DEFAULT_PRESET']

        # Validate output format
        if output_format not in current_app.config['OUTPUT_FORMATS']:
            output_format = current_app.config['OUTPUT_FORMAT_DEFAULT']

    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid options: {str(e)}'}), 400

    # Generate safe filename
    safe_filename = FileValidator.get_safe_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    input_path = os.path.join(upload_folder, f"original_{safe_filename}")
    output_path = os.path.join(upload_folder, f"optimized_{safe_filename}")

    try:
        # Save uploaded file
        file.save(input_path)

        # Validate the uploaded file
        validation_result = FileValidator.validate_upload(file, input_path)

        if not validation_result['valid']:
            # Clean up invalid file
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({'error': validation_result['error']}), 400

        # Prepare optimization options
        options = {
            'quality': quality,
            'resize_percent': resize_percent,
            'strip_metadata': strip_metadata,
            'auto_orient': auto_orient,
            'preset': preset,
            'sharpen': sharpen,
            'output_format': output_format
        }

        # Optimize the image
        optimization_result = ImageOptimizer.optimize_image(input_path, output_path, options)

        if not optimization_result['success']:
            # Clean up on failure
            FileCleanup().cleanup_specific_files([input_path, output_path])
            return jsonify({'error': f"Optimization failed: {optimization_result.get('error', 'Unknown error')}"}), 500

        # Update safe filename if format changed
        final_filename = safe_filename
        if optimization_result.get('format_converted'):
            base_name = os.path.splitext(safe_filename)[0]
            final_filename = f"{base_name}.{output_format}"

        # Prepare response
        response_data = {
            'success': True,
            'original_filename': file.filename,
            'safe_filename': final_filename,
            'original_size': optimization_result['original_size'],
            'optimized_size': optimization_result['optimized_size'],
            'reduction_bytes': optimization_result['reduction_bytes'],
            'reduction_percent': optimization_result['reduction_percent'],
            'format': optimization_result['format'],
            'output_format': optimization_result['output_format'],
            'format_converted': optimization_result['format_converted'],
            'original_width': optimization_result['original_width'],
            'original_height': optimization_result['original_height'],
            'width': optimization_result['width'],
            'height': optimization_result['height'],
            'resized': optimization_result['resized'],
            'metadata_stripped': optimization_result['metadata_stripped'],
            'auto_oriented': optimization_result['auto_oriented'],
            'preset': optimization_result['preset'],
            'quality_used': optimization_result['quality_used'],
            'sharpened': optimization_result['sharpened'],
            'sharpen_amount': optimization_result['sharpen_amount'],
            'download_url': f'/download/{final_filename}',
            'preview_url': f'/preview/optimized/{final_filename}'
        }

        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error processing upload: {e}")
        # Clean up on error
        FileCleanup().cleanup_specific_files([input_path, output_path])
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@main_bp.route('/download/<filename>')
def download_image(filename):
    """
    Download the optimized image and delete temp files after response.

    Args:
        filename (str): Safe filename to download

    Returns:
        File download response
    """
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        input_path = os.path.join(upload_folder, f"original_{filename}")
        output_path = os.path.join(upload_folder, f"optimized_{filename}")

        if not os.path.exists(output_path):
            return jsonify({'error': 'File not found'}), 404

        # Send file and cleanup after response if configured
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=f"optimized_{filename}"
        )

        # Delete files immediately after sending if configured
        if current_app.config['DELETE_AFTER_RESPONSE']:
            @response.call_on_close
            def cleanup_files():
                FileCleanup().cleanup_specific_files([input_path, output_path])

        return response

    except Exception as e:
        current_app.logger.error(f"Error downloading file: {e}")
        return jsonify({'error': 'Download failed'}), 500


@main_bp.route('/preview/<file_type>/<filename>')
def preview_image(file_type, filename):
    """
    Preview original or optimized image.

    Args:
        file_type (str): 'original' or 'optimized'
        filename (str): Safe filename

    Returns:
        Image file for preview
    """
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']

        if file_type not in ['original', 'optimized']:
            return jsonify({'error': 'Invalid file type'}), 400

        file_path = os.path.join(upload_folder, f"{file_type}_{filename}")

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, mimetype='image/jpeg')

    except Exception as e:
        current_app.logger.error(f"Error previewing file: {e}")
        return jsonify({'error': 'Preview failed'}), 500


@main_bp.route('/cleanup-all', methods=['POST'])
def cleanup_all():
    """
    Clean up all files in the uploads folder.
    Called on page refresh/load to ensure no leftover files.

    Returns:
        JSON response with cleanup status
    """
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']

        if not os.path.exists(upload_folder):
            return jsonify({'success': True, 'message': 'Upload folder does not exist'}), 200

        removed_count = 0
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            try:
                os.remove(file_path)
                removed_count += 1
            except Exception as e:
                current_app.logger.error(f"Error removing file {filename}: {e}")

        current_app.logger.info(f"Page refresh cleanup: {removed_count} files removed")

        return jsonify({
            'success': True,
            'message': f'Cleaned up {removed_count} files',
            'count': removed_count
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error during cleanup-all: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@main_bp.route('/health')
def health_check():
    """Health check endpoint for Docker/monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'image-optimization'
    }), 200
