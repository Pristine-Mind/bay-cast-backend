import segno
from io import BytesIO
from django.core.files import File


def generate_qr(id: str, name: str) -> File:
    """
    Generate a QR image with the provided ID and name.

    This function creates a QR code containing the ID and name information
    and saves it as a PNG image file.

    Args:
        id (str): The ID of the product.
        name (str): The name of the product.

    Returns:
        File: The QR image file.
    """

    # Combine ID and name into a single string to be encoded in the QR code
    data = f"ID: {id}, Name: {name}"

    # Generate the QR code with the specified error correction level
    qr = segno.make(data, error='h')  # 'h' stands for high error correction

    # Create a BytesIO object to hold the QR code image data
    qr_io = BytesIO()

    # Save the QR code image to the BytesIO object in PNG format
    qr.save(qr_io, kind='png', scale=10, border=4)

    # Ensure the BytesIO object is positioned at the start
    qr_io.seek(0)

    # Create a Django File object from the BytesIO object
    qr_image = File(qr_io, name=f'{id}_{name}.png')

    return qr_image
