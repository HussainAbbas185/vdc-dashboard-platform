
import os
import io
import zipfile
from PIL import Image

def compress_files(files_dict):
    """
    Compresses a dictionary of {filename: bytes_content} into a ZIP file.
    Returns: BytesIO object of the zip file.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for fname, fcontent in files_dict.items():
            zip_file.writestr(fname, fcontent)
    zip_buffer.seek(0)
    return zip_buffer

def extract_zip(zip_bytes):
    """
    Extracts files from a ZIP BytesIO object.
    Returns: Dictionary {filename: bytes_content}
    """
    extracted_files = {}
    try:
        with zipfile.ZipFile(zip_bytes) as z:
            for filename in z.namelist():
                if not filename.endswith('/'): # Skip directories
                    extracted_files[filename] = z.read(filename)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return None
    return extracted_files

def convert_image(image_bytes, target_format):
    """
    Converts image bytes to target format (PNG, JPEG, WEBP, BMP).
    Returns: (converted_bytes, new_filename_extension)
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if saving as JPEG (handle transparency rejection)
        if target_format.upper() in ['JPEG', 'JPG'] and img.mode in ['RGBA', 'P']:
            img = img.convert('RGB')
            
        output_buffer = io.BytesIO()
        save_format = target_format.upper()
        if save_format == 'JPG': save_format = 'JPEG'
        
        img.save(output_buffer, format=save_format)
        output_buffer.seek(0)
        
        ext = '.' + target_format.lower()
        if ext == '.jpeg': ext = '.jpg'
        
        return output_buffer, ext
        return None, None

def convert_document(file_bytes, input_ext, target_ext):
    """
    Converts documents between PDF and DOCX.
    Supported: PDF -> DOCX, DOCX -> PDF
    """
    import tempfile
    
    # 1. Setup Temp Files
    with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as tmp_in:
        tmp_in.write(file_bytes)
        input_path = tmp_in.name
    
    output_path = input_path.replace(input_ext, target_ext)
    
    try:
        # 2. PDF -> DOCX
        if input_ext == '.pdf' and target_ext == '.docx':
            from pdf2docx import Converter
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
        # 3. DOCX -> PDF
        elif input_ext == '.docx' and target_ext == '.pdf':
            from docx2pdf import convert
            # docx2pdf converts in-place or to directory, let's specify output
            convert(input_path, output_path)
            
        # 4. Read Result
        if os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                result_bytes = f.read()
            # Cleanup
            try:
                os.remove(input_path)
                os.remove(output_path)
            except: pass
            return result_bytes, target_ext
            
    except Exception as e:
        print(f"Doc Conversion Error: {e}")
        return None, None
    
    return None, None
