from django.conf import settings
from permit import Permit


def get_permit_client():
    pdp_url = settings.PERMIT_PDP_URL
    api_key = settings.PERMIT_API_KEY
    if not api_key:
        raise ValueError("PERMIT_API_KEY was not set in django settings.")
    return Permit(
        pdp=pdp_url,
        token=api_key
    )

permit_client = get_permit_client()