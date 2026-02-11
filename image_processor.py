"""
Image optimization module using Pillow (PIL).
Handles JPEG, PNG, and WebP optimization with advanced options.
"""
import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from flask import current_app


class ImageOptimizer:
    """Image optimization handler using Pillow."""

    @staticmethod
    def optimize_image(input_path, output_path, options=None):
        """
        Optimize an image based on its format with configurable options.

        Args:
            input_path (str): Path to input image
            output_path (str): Path to save optimized image
            options (dict): Optimization options:
                - quality (int): Quality for JPEG/WebP (1-95)
                - resize_percent (int): Resize percentage (10-200)
                - strip_metadata (bool): Strip EXIF/metadata
                - auto_orient (bool): Auto-orient based on EXIF
                - preset (str): 'speed', 'balanced', or 'max_quality'
                - sharpen (int): Sharpen intensity (0-100)
                - output_format (str): Output format ('same', 'jpeg', 'png', 'webp')

        Returns:
            dict: Optimization results with before/after sizes and format info
        """
        # Set default options
        if options is None:
            options = {}

        quality = options.get('quality', current_app.config['DEFAULT_QUALITY'])
        resize_percent = options.get('resize_percent', current_app.config['DEFAULT_RESIZE_PERCENT'])
        strip_metadata = options.get('strip_metadata', current_app.config['STRIP_METADATA_DEFAULT'])
        auto_orient = options.get('auto_orient', current_app.config['AUTO_ORIENT_DEFAULT'])
        preset = options.get('preset', current_app.config['DEFAULT_PRESET'])
        sharpen = options.get('sharpen', current_app.config['SHARPEN_DEFAULT'])
        output_format = options.get('output_format', current_app.config['OUTPUT_FORMAT_DEFAULT'])

        # Get preset settings if specified
        preset_settings = current_app.config['PRESETS'].get(preset, current_app.config['PRESETS']['balanced'])

        try:
            # Get original file size
            original_size = os.path.getsize(input_path)

            # Open image with Pillow
            with Image.open(input_path) as img:
                # Store original format and mode
                original_format = img.format
                original_mode = img.mode

                # Store original EXIF data if needed
                exif_data = None
                if not strip_metadata and hasattr(img, 'info') and 'exif' in img.info:
                    exif_data = img.info['exif']

                # Auto-orient based on EXIF orientation
                if auto_orient:
                    img = ImageOps.exif_transpose(img)

                # Strip metadata by removing all info
                if strip_metadata:
                    # Clear the info dictionary to remove all metadata
                    img.info = {}

                # Get original dimensions
                original_width, original_height = img.size

                # Resize if needed
                new_width, new_height = original_width, original_height
                if resize_percent != 100:
                    new_width = int(original_width * resize_percent / 100)
                    new_height = int(original_height * resize_percent / 100)
                    img = img.resize((new_width, new_height), Image.LANCZOS)

                # Apply sharpening if requested
                if sharpen > 0:
                    img = ImageOptimizer._apply_sharpening(img, sharpen)

                # Determine output format
                if output_format == 'same':
                    target_format = original_format
                else:
                    target_format = output_format.upper()
                    # Update output path extension if format changed
                    base_name = os.path.splitext(output_path)[0]
                    output_path = f"{base_name}.{output_format}"

                # Convert RGBA to RGB for JPEG (JPEG doesn't support transparency)
                if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img

                # Final metadata strip - ensure info dict is clear if stripping
                if strip_metadata:
                    img.info = {}

                # Optimize based on target format
                save_kwargs = {}
                if not strip_metadata and exif_data and target_format == original_format:
                    # Only preserve EXIF if keeping same format
                    save_kwargs['exif'] = exif_data

                if target_format in ['JPEG', 'JPG']:
                    result = ImageOptimizer._optimize_jpeg(
                        img, output_path, quality, preset_settings, save_kwargs
                    )
                elif target_format == 'PNG':
                    result = ImageOptimizer._optimize_png(
                        img, output_path, preset_settings, save_kwargs
                    )
                elif target_format == 'WEBP':
                    result = ImageOptimizer._optimize_webp(
                        img, output_path, quality, preset_settings, save_kwargs
                    )
                else:
                    # Fallback: save as JPEG
                    result = ImageOptimizer._optimize_jpeg(
                        img, output_path, quality, preset_settings, save_kwargs
                    )

                # Get optimized file size
                optimized_size = os.path.getsize(output_path)

                # Calculate reduction
                reduction_bytes = original_size - optimized_size
                reduction_percent = (reduction_bytes / original_size * 100) if original_size > 0 else 0

                return {
                    'success': True,
                    'original_size': original_size,
                    'optimized_size': optimized_size,
                    'reduction_bytes': reduction_bytes,
                    'reduction_percent': round(reduction_percent, 2),
                    'format': original_format,
                    'output_format': target_format,
                    'format_converted': output_format != 'same',
                    'original_width': original_width,
                    'original_height': original_height,
                    'width': new_width,
                    'height': new_height,
                    'mode': original_mode,
                    'resized': resize_percent != 100,
                    'metadata_stripped': strip_metadata,
                    'auto_oriented': auto_orient,
                    'preset': preset,
                    'quality_used': quality if target_format in ['JPEG', 'WEBP'] else None,
                    'sharpened': sharpen > 0,
                    'sharpen_amount': sharpen
                }

        except Exception as e:
            current_app.logger.error(f"Error optimizing image: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def _optimize_jpeg(img, output_path, quality, preset_settings, save_kwargs):
        """
        Optimize JPEG image.

        Args:
            img: PIL Image object
            output_path (str): Path to save optimized image
            quality (int): Quality setting
            preset_settings (dict): Preset configuration
            save_kwargs (dict): Additional save arguments (e.g., exif)

        Returns:
            dict: Optimization settings used
        """
        # Use quality from preset if not custom
        jpeg_quality = preset_settings.get('jpeg_quality', quality)

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save with optimization
        img.save(
            output_path,
            'JPEG',
            quality=jpeg_quality,
            optimize=True,
            progressive=True,
            **save_kwargs
        )

        return {
            'quality': jpeg_quality,
            'progressive': True,
            'optimize': True
        }

    @staticmethod
    def _optimize_png(img, output_path, preset_settings, save_kwargs):
        """
        Optimize PNG image.

        Args:
            img: PIL Image object
            output_path (str): Path to save optimized image
            preset_settings (dict): Preset configuration
            save_kwargs (dict): Additional save arguments

        Returns:
            dict: Optimization settings used
        """
        compress_level = preset_settings.get('png_compress_level', 9)

        # Save with optimization
        img.save(
            output_path,
            'PNG',
            optimize=True,
            compress_level=compress_level,
            **save_kwargs
        )

        return {
            'optimize': True,
            'compress_level': compress_level
        }

    @staticmethod
    def _optimize_webp(img, output_path, quality, preset_settings, save_kwargs):
        """
        Optimize WebP image.

        Args:
            img: PIL Image object
            output_path (str): Path to save optimized image
            quality (int): Quality setting
            preset_settings (dict): Preset configuration
            save_kwargs (dict): Additional save arguments

        Returns:
            dict: Optimization settings used
        """
        # Use quality from preset if not custom
        webp_quality = preset_settings.get('webp_quality', quality)
        webp_method = preset_settings.get('webp_method', 6)

        # Save with optimization
        img.save(
            output_path,
            'WEBP',
            quality=webp_quality,
            method=webp_method,
            **save_kwargs
        )

        return {
            'quality': webp_quality,
            'method': webp_method
        }

    @staticmethod
    def _apply_sharpening(img, sharpen_amount):
        """
        Apply sharpening to an image.

        Args:
            img: PIL Image object
            sharpen_amount (int): Sharpen intensity (0-100)

        Returns:
            PIL Image object: Sharpened image
        """
        if sharpen_amount <= 0:
            return img

        # Use UnsharpMask for better quality sharpening
        # sharpen_amount: 0-100 maps to radius: 0-5, percent: 0-150, threshold: 0-3
        radius = (sharpen_amount / 100) * 2.5  # 0 to 2.5
        percent = 50 + (sharpen_amount / 100) * 100  # 50 to 150
        threshold = int((sharpen_amount / 100) * 3)  # 0 to 3

        try:
            sharpened = img.filter(ImageFilter.UnsharpMask(
                radius=radius,
                percent=int(percent),
                threshold=threshold
            ))
            return sharpened
        except Exception as e:
            current_app.logger.warning(f"Error applying sharpening: {e}. Using basic sharpen.")
            # Fallback to basic sharpen filter
            return img.filter(ImageFilter.SHARPEN)

    @staticmethod
    def get_image_info(image_path):
        """
        Get basic information about an image.

        Args:
            image_path (str): Path to image file

        Returns:
            dict: Image information
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height
                }
        except Exception as e:
            current_app.logger.error(f"Error getting image info: {e}")
            return None
