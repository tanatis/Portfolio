from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from portfolio.account.forms import AppUserCreationForm, ProfileEditForm, AppUserDeleteForm
from portfolio.account.models import Profile, AppUserHistory

UserModel = get_user_model()


class SignUpView(views.CreateView):
    model = UserModel
    template_name = 'account/user-register.html'
    success_url = reverse_lazy('login')
    form_class = AppUserCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(request, 'You already have an account. No need to register again.')
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


class SignInView(auth_views.LoginView):
    template_name = 'account/user-login.html'


class SignOutView(auth_views.LogoutView):
    pass


class AppUserChangePassword(auth_views.PasswordChangeView):
    template_name = 'account/change-password.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('profile details', args=[pk])


class ProfileDetailsView(views.DetailView):
    template_name = 'account/profile-details.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object
        context['pk'] = self.object.pk

        return context


class ProfileEditView(views.UpdateView):
    template_name = 'account/profile-edit.html'
    model = Profile
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if self.request.user != profile.user:
            messages.error(request, 'You can only edit your own profile')
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)


@login_required
def user_delete(request, pk):
    user = UserModel.objects.filter(pk=pk).get()

    if request.user != user:
        messages.warning(request, 'You can only delete your own account!')
        return redirect('restricted')

    if request.method == 'GET':
        form = AppUserDeleteForm(instance=user)
    else:
        form = AppUserDeleteForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'account/user-delete.html', context)


def account_history(request, pk):
    transaction_history = AppUserHistory.objects.filter(to_user_id=request.user.pk)

    context = {
        'transaction_history': transaction_history,
    }

    return render(request, 'account/transaction-history.html', context)
