from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm
from agents.mixins import OrganiserAndLoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = 'leads'


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # ToDo -> send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")


# Function Base CRUD
def landing_page(request):
    return render(request, 'landing.html')


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    return render(request, "leads/lead_list.html", context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_detail.html", context)


def lead_create(request):
    form = LeadModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/leads")
    context = {
        "form": form,
    }
    return render(request, "leads/lead_create.html", context)


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(request.POST or None, instance=lead)
    if form.is_valid():
        form.save()
        return redirect('/leads')
    context = {
        "lead": lead,
        "form": form,
    }
    return render(request, "leads/lead_update.html", context)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")
