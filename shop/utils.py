# file for various helper functions


def get_item_image_upload_location(instance, filename):
    extension = filename.split('.')[1]
    file_path = f'items/{instance.category}/{instance.id}.{extension}'
    return file_path
