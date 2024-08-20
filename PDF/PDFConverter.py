import fitz  # PyMuPDF
import os

class PDFConverter:
    def __init__(self, pdf_path, output_folder, zoom_x=2.0, zoom_y=2.0):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.zoom_x = zoom_x  # Horizontal zoom
        self.zoom_y = zoom_y  # Vertical zoom
        self.images = []  # List to store image paths

    def convert_pdf_to_images(self):
        try:
            # Open the PDF file
            pdf_document = fitz.open(self.pdf_path)
            num_pages = pdf_document.page_count

            # Ensure output folder exists
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            # Convert each page to an image
            for page_num in range(num_pages):
                page = pdf_document[page_num]
                # Apply zoom to increase image resolution
                mat = fitz.Matrix(self.zoom_x, self.zoom_y)
                pix = page.get_pixmap(matrix=mat)
                image_name = f'page_{page_num + 1}.png'
                image_path = os.path.join(self.output_folder, image_name)
                pix.save(image_path)
                # Append the image path to the list
                self.images.append(image_path)

            print(f"PDF converted successfully! Images saved in: {self.output_folder}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_image_paths(self):
        return self.images

