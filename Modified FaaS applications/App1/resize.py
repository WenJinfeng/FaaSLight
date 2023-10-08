def resize_image(image, resize_width, resize_height):
    """Resize an image

    :param image:
    :type image: wand.image.Image
    :param resize_width:
    :type resize_width: int or float
    :param resize_height:
    :type resize_height: int or float
    :return:
    :rtype: wand.image.Image
    """
    if resize_width == image.width and resize_height == image.height:
        return image

    original_ratio = image.width / float(image.height)
    resize_ratio = resize_width / float(resize_height)

    # We stick to the original ratio here, regardless of what the resize ratio is
    if original_ratio > resize_ratio:
        # If width is larger, we base the resize height as a function of the ratio of the width
        resize_height = int(round(resize_width / original_ratio))
    else:
        # Otherwise, we base the width as a function of the ratio of the height
        resize_width = int(round(resize_height * original_ratio))

    if ((image.width - resize_width) + (image.height - resize_height)) < 0:
        filter_name = 'mitchell'
    else:
        filter_name = 'lanczos2'

    image.resize(width=resize_width, height=resize_height, filter=filter_name, blur=1)

    return image