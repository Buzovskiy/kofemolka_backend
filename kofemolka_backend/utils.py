import os


def post_delete_image(sender, instance, field_name='image', *args, **kwargs):
    """When we delete Location instance, delete old image file """
    try:
        getattr(instance, field_name).delete(save=False)
    except:
        pass


def pre_save_image(sender, instance, field_name='image', *args, **kwargs):
    """When update Location, delete old image file.Instance old image file will delete from os """
    try:
        old_img = getattr(instance.__class__.objects.get(pk=instance.pk), field_name).path
        try:
            new_img = getattr(instance, field_name).path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass
