from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.http import Http404


class StaffRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(StaffRequiredMixin, self).as_view()
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super(StaffRequiredMixin, self).dispatch(self.request, *args, **kwargs)
        else:
            Http404


class LoginRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(LoginRequiredMixin, self).as_view()
        return staff_member_required(view)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(self.request, *args, **kwargs)
