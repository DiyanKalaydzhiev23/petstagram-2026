from django.contrib.auth.mixins import UserPassesTestMixin


class CheckUserIsOwner(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user == self.get_object().user
