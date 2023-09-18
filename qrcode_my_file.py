import qrcode
import random
import string
import time
import schedule
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer

###  ----------------------------------------------------------------------

from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from qrcode.image.styles.colormasks import ImageColorMask
###  ----------------------------------------------------------------------


class QRCodeGenerator:
    def __init__(self, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border
        self.filename = None

    def file_name_generator(self, extension):
        timestamp = int(time.time())
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        unique_name = f"generated_by_{timestamp}_{random_string}.{extension}"
        return unique_name

    def Color_Style(self, color_style):
        if color_style == "SolidFillColorMask":
            return SolidFillColorMask()
        elif color_style == "RadialGradiantColorMask":
            return RadialGradiantColorMask()
        elif color_style == "SquareGradiantColorMask":
            return SquareGradiantColorMask()
        elif color_style == "HorizontalGradiantColorMask":
            return HorizontalGradiantColorMask()
        elif color_style == "VerticalGradiantColorMask":
            return VerticalGradiantColorMask()
        elif color_style == "ImageColorMask":
            return ImageColorMask()

    def Style(self, style):
        if style == "RoundedModuleDrawer":
            return RoundedModuleDrawer()
        elif style == "RadialGradiantColorMask":
            return RadialGradiantColorMask()
        elif style == "SquareModuleDrawer":
            return SquareModuleDrawer()
        elif style == "GappedSquareModuleDrawer":
            return GappedSquareModuleDrawer()
        elif style == "CircleModuleDrawer":
            return CircleModuleDrawer()
        elif style == "VerticalBarsDrawer":
            return VerticalBarsDrawer()
        elif style == "HorizontalBarsDrawer":
            return HorizontalBarsDrawer()


    def generate_qrcode(self, text, background_color, foreground_color, style, width, height, file_type, color_style):

        if style == "SquareModuleDrawer":
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=int(width) // self.version,
                border=self.border,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color=foreground_color, back_color=background_color)

        else:
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=(int(width)/10),
                border=self.border,
            )
            qr.add_data(text)
            qr.make(fit=True)
            drawer = self.Style(style)
            # print(type(drawer))
            color_mask = self.Color_Style(color_style)
            # print(color_mask)
            try:
                img = qr.make_image(image_factory=StyledPilImage, module_drawer=drawer, color_mask=color_mask)

            except Exception as e:
                print(e)



        self.filename = self.file_name_generator(file_type)
        if file_type == 'pdf':
            self.save_file(img=img, filename=self.filename, file_type='pdf')
        else:
            img.save(f"static/{self.filename}")
        return self.filename
    def cleanup(self):

        if self.filename:
            try:
                os.remove(f"static/{self.filename}")
            except FileNotFoundError:
                pass

        self.filename = None

    def save_file(self, img, filename, file_type):

        # Create a PDF file
        c = canvas.Canvas(f"static/{filename}", pagesize=letter)

        # Calculate the aspect ratio to fit the QR code within the PDF page
        width, height = img.size
        aspect_ratio = width / height
        if aspect_ratio > 1:
            qr_width = 400
            qr_height = 400 / aspect_ratio
        else:
            qr_height = 400
            qr_width = 400 * aspect_ratio

            # Save the StyledPilImage as a temporary file
        temp_filename = "temp.png"
        img.save(temp_filename)

        # Draw the QR code on the PDF page
        c.drawImage(temp_filename, 100, 400 - qr_height, width=qr_width, height=qr_height)

        # Save the PDF
        c.save()

        # Remove the temporary image
        os.remove(temp_filename)

    def delete_files(self):
        folder_path = "static/"  # The folder where the files are located
        extensions = (".png", ".jpg")  # List of file extensions to delete

        for filename in os.listdir(folder_path):
            if filename.endswith(extensions):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


    # Schedule the cleanup function to run daily at 00:00 hrs
# schedule.every().day.at("00:00").do(QRCodeGenerator.delete_files())
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#
if __name__ == "__main__":
    # QRCodeGenerator().delete_files()
    qrcode_generator = QRCodeGenerator()
    # schedule.every().day.at("00:00").do(QRCodeGenerator.delete_files())
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
    qrcode_generator.generate_qrcode(text="jhviuahfwioj xoijaigrs", background_color="red",
                                     foreground_color="#23dda0",
                                     style="CircleModuleDrawer",
                                     color_style="VerticalGradiantColorMask",
                                     width=350,
                                     height=350,
                                     file_type="pdf"
                                     )


