from django.shortcuts import render, reverse
from django.views import generic
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import LoginAndOrganiserRequiredMixin


class SignUpView(generic.CreateView):
  template_name = 'registration/signup.html'
  from_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('leads:lead_list')

class LandingPageView(generic.TemplateView):
  template_name = 'landing_page.html'


class LeadListView(LoginRequiredMixin,generic.ListView):
  template_name = 'leads/lead_list.html'
  context_object_name = 'leads'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      queryset = queryset.filter(agent__user=user)
    return  queryset


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'leads/lead_detail.html'
  context_object_name = 'lead'

  def get_queryset(self):
    return Lead.objects.all()


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name = 'leads/lead_update.html'
  form_class = LeadModelForm

  def get_success_url(self):
    return reverse('leads:lead_list')
  
  def get_queryset(self):
    organisation = self.request.user.userprofile
    queryset = Lead.objects.filter(organisation=organisation)
    return queryset
  
  def form_valid(self, form):
    lead = form.save(commit=False)
    lead.organisation = self.request.user.userprofile
    lead.save()
    return super(LeadUpdateView, self).form_valid(form)
  

class LeadCreateView(LoginAndOrganiserRequiredMixin, generic.CreateView):
  template_name = 'leads/lead_create.html'
  form_class = LeadModelForm

  def get_queryset(self):
    organisation = self.request.user.userprofile
    queryset = Lead.objects.filter(organisation=organisation)
    return queryset

  def get_success_url(self):
    return reverse('leads:lead_list')

  def form_valid(self, form):
    lead = form.save(commit=False)
    lead.organisation = self.request.user.userprofile
    lead.save()
    return super(LeadCreateView, self).form_valid(form)

  
class LeadDeleteView(LoginAndOrganiserRequiredMixin, generic.DeleteView):
  template_name = 'leads/lead_delete.html'
  context_object_name = 'lead'

  def get_success_url(self):
    return reverse('leads:lead_list')

  def get_queryset(self):
    return Lead.objects.all()


