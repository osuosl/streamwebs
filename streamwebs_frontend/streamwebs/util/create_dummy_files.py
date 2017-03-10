from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_temporary_image():
    io = StringIO.StringIO()
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new('RGBA', size, color)
    image.save(io, format='JPEG')
    image_file = InMemoryUploadedFile(io, None, 'foo.jpg', 'jpeg', io.len,
                                      None)
    image_file.seek(0)
    return image_file


def get_temporary_text_file():
    io = StringIO.StringIO()
    io.write('This is a dummy file that is full of dummy text.')
    text_file = InMemoryUploadedFile(io, None, 'foo.pdf', 'pdf', io.len, None)
    text_file.seek(0)
    return text_file
