import qrcode
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
    data = f"ID: {id}, Name: {name}"
    qr = qrcode.make(data)
    qr_io = BytesIO()
    qr.save(qr_io, 'PNG')
    qr_image = File(qr_io, name=f'{id}_{name}.png')
    return qr_image
