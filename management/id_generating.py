import random
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

from .models import Citizen, IDCardRegistration



def generate_unique_nid_number(citizen):
    # Generate a unique NID number based on the citizen's attributes
    gender_prefix = '1' if citizen.gender == Citizen.Gender.MALE else '2' if citizen.gender == Citizen.Gender.FEMALE else '0'
    birthdate_part = citizen.birthdate.strftime('%Y%m%d')
    taken_count_part = citizen.id_registrations.filter(status=IDCardRegistration.Status.APPROVED).count() + 1
    random_part = random.randint(1000000, 9999999)  # You can adjust the range as needed

    # Combine the parts to create the NID number
    nid_number = f'{taken_count_part}{birthdate_part}{gender_prefix}{random_part}'

    # Check if the generated NID number already exists
    while Citizen.objects.filter(nid_number=nid_number).exists():
        random_part = random.randint(1000000, 9999999)
        nid_number = f'{taken_count_part}{birthdate_part}{gender_prefix}{random_part}'

    return nid_number



def generate_qr_code(citizen, placeofissue):
    # Format the data for the QR code
    qr_data = {
        "NID Number": citizen.nid_number,
        "First Name": citizen.first_name,
        "Last Name": citizen.last_name,
        "Gender": citizen.gender,
        "Birthdate": citizen.birthdate.strftime("%Y-%m-%d"),
        "Place of Issue": placeofissue.commune_name+", Burundi",
    }
    formatted_data = "\n".join([f"{key}: {value}" for key, value in qr_data.items()])
    
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(formatted_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Get the media root directory from settings.py
    media_root = settings.MEDIA_ROOT

    # Define the directory where you want to save the QR code images
    qr_code_images_dir = os.path.join(media_root, 'citizen/qr_codes')

    # Make sure the directory exists; create it if it doesn't
    if not os.path.exists(qr_code_images_dir):
        os.makedirs(qr_code_images_dir)

    # Define the filename for the QR code image
    qr_code_filename = f'{citizen.nid_number}_qr_code.png'

    # Build the full path to save the image
    qr_code_path = os.path.join(qr_code_images_dir, qr_code_filename)

    # Save the QR code image to the configured media directory
    qr_img.save(qr_code_path)

    # Return the path to the saved QR code image
    return qr_code_path