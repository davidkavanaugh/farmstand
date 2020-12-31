from django.http import QueryDict, JsonResponse
import stripe
import os
from .views import User
from urllib import parse
from django.contrib import messages

stripe.api_key = os.getenv("STRIPE_API_KEY")

def CreateStripeUser(email, first_name, last_name, street_2, city, state, zip_code):
    stripe_user = stripe.Account.create(
        type='express',
        country="US",
        email=email,
        individual={
            "id_number": "000000000",
            "first_name": first_name,
            "last_name": last_name,
            "address": {
                "line1": "address_full_match​",
                "line2": street_2,
                "city": city,
                "state": state,
                "postal_code": zip_code
            }
        },
        business_type="individual",
        default_currency="USD"
    )
    return stripe_user

def CreateStripeLink(stripe_userId):
    stripe_link = stripe.AccountLink.create(
        account=stripe_userId,
        refresh_url=f"http://54.241.134.58/users/refresh/{stripe_userId}",
        return_url="http://54.241.134.58/users/sign-in",
        type="account_onboarding",
    )
    return stripe_link

def RefreshStripeUser(request, stripeId):
    user = User.objects.get(stripeId=stripeId)
    stripe_user = CreateStripeUser(user.email, user.first_name, user.last_name, user.street_2, user.city, user.state, user.zip_codes)
    stripe_link = CreateStripeLink(stripe_user.id)
    return redirect(stripe_link.url)

def StripeReady(stripe_user):
    if stripe_user.details_submitted == True and stripe_user.charges_enabled == True and stripe_user.capabilities.card_payments == "active" and stripe_user.capabilities.transfers == "active":
        return True
    else:
        return False

def FindUserByEmail(email):
    # get user by email from db
    user = User.objects.filter(email=email)
    if user:
        return user[0]
    else: 
        return False

def ValidatePatchRequest(request, user_id):
    errors = User.objects.update_validator(request.POST, request.FILES, user_id)
    if len(errors) > 0:
        for key, value in errors.items():
            print(f'error: {key}, message: {value}')
            messages.error(request, value, extra_tags=key)
        return True
    else:
        return False