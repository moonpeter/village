from allauth.socialaccount.providers.apple.provider import AppleProvider


class CustomAppleProvider(AppleProvider):
    def extract_common_fields(self, data):
        fields = {"email": data.get("email")}
        # If the name was provided
        name = data.get("name")
        if name:
            fields["first_name"] = data.get("family_name", "")
            fields["last_name"] = data.get("given_name", "")

        return fields


provider_classes = [CustomAppleProvider]
