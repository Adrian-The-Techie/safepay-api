from rest_framework import serializers

from payments.models import Payout
class PayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payout
        exclude=["user","payin_ref_no","responsePayload","callbackPayload",]