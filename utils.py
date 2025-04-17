def correct_serial(text):
    """Fix common OCR mistakes"""
    corrections = {
        'O': '0', 'I': '1', 'l': '1',
        'B': '8', 'Z': '2', 'S': '5'
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text.strip("*#")  # Remove special chars