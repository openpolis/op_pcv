from django.conf import settings

def main_settings(request):


    return {
        "DEBUG": settings.DEBUG,
        "TEMPLATE_DEBUG": settings.TEMPLATE_DEBUG,

        }