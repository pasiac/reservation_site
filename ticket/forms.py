from creditcards.forms import (CardExpiryField, CardNumberField,
                               SecurityCodeField)
from django.forms import Form, ModelForm

from ticket.models import TicketReservation


class TicketReservationForm(ModelForm):
    class Meta:
        model = TicketReservation
        fields = ["quantity", "ticket"]


class PaymentForm(Form):
    cc_number = CardNumberField(label="Card Number")
    cc_expiry = CardExpiryField(label="Expiration Date")
    cc_code = SecurityCodeField(label="CVV/CVC")
