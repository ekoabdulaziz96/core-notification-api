from constants.messages import resp_success
from cores.views import BaseView
from serializers.emails import EmailSerializer


class ManageEmail(BaseView):
    serializer_class = EmailSerializer

    def save(self):
        self._validate_header_json()
        self.payload = self.request.json if self.request.json else {}
        self.serializer = self.serializer_class()

        self.serializer.is_valid(self.payload)
        self.serializer.save()

        return self.serializer.data(), resp_success.success
