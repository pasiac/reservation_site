from django.forms import ModelForm, Form
from ticket.models import TicketReservation
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField


class TicketReservationForm(ModelForm):
    class Meta:
        model = TicketReservation
        fields = ["quantity", "ticket"]

class PaymentForm(Form):
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')