import os
from rest_framework.response import Response
from rest_framework import status


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


def validate_api_token(request, valid_token):
    """
    Validates the `api_token` in the request query parameters.

    Args:
        request (HttpRequest): The incoming HTTP request.
        valid_token (str): The valid token to compare against.

    Returns:
        None or Response: Returns None if valid, otherwise a 401 Response.
    """
    api_token = request.query_params.get('api_token', None)
    if not api_token or api_token != valid_token:
        return Response(
            {"detail": "Authentication error: Invalid or missing api_token."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return None
