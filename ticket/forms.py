from creditcards.forms import CardExpiryField, CardNumberField, SecurityCodeField
from django.forms import Form, ModelForm

from ticket.models import TicketReservation, Ticket


class TicketReservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop("event_id")
        super().__init__(*args, **kwargs)
        self.fields["ticket"].queryset = Ticket.objects.filter(event__pk=event_id)

    class Meta:
        model = TicketReservation
        fields = ["quantity", "ticket"]


class PaymentForm(Form):
    cc_number = CardNumberField(label="Card Number")
    cc_expiry = CardExpiryField(label="Expiration Date")
    cc_code = SecurityCodeField(label="CVV/CVC")
