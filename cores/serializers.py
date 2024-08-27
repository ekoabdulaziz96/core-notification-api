from marshmallow import Schema


class Serializer(Schema):
    def __init__(self, instance=None, **kwargs):
        self.instance = instance
        super().__init__(**kwargs)

    def is_valid(self, payload):
        self.validated_data = self.load(payload)

    def save(self, commit=False):
        self.instance = self.model(**self.validated_data)
        self.instance.save(commit)

    def update(self, commit=False):
        self.instance.update(**self.validated_data, commit=commit)

    def data(self):
        if self.instance:
            return self.dump(self.instance)
        else:
            return self.dump(self.validated_data)
