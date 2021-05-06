from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_has_value(self, customer, timestamp):
        return (six.text_type(customer.pk)+six.text_type(timestamp) + six.text_type(customer.company_name))

generate_token = TokenGenerator()