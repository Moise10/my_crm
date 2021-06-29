from django.shortcuts import render, reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import LoginAndOrganiserRequiredMixin


class AgentListView(LoginAndOrganiserRequiredMixin,generic.ListView):
  template_name = 'agents/agent_list.html'
  context_object_name = 'agents'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Agent.objects.filter(organisation=user.userprofile)
    return queryset


class AgentDetailView(LoginAndOrganiserRequiredMixin, generic.DetailView):
  template_name = 'agents/agent_detail.html'
  context_object_name = 'agent'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Agent.objects.filter(organisation=user.userprofile)
    return queryset


class AgentCreateView(LoginAndOrganiserRequiredMixin, generic.CreateView):
  template_name = 'agents/agent_create.html'
  form_class = AgentModelForm

  def get_success_url(self):
    return reverse('agents:agent_list')

  def form_valid(self, form):
    user = form.save(commit=False)
    user.is_organiser = False
    user.is_agent = True
    user.save()
    Agent.objects.create(
      user=user,
      organisation=self.request.user.userprofile
    )
    return super(AgentCreateView, self).form_valid(form)

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Agent.objects.filter(organisation=user.userprofile)
    return queryset


class AgentUpdateView(LoginAndOrganiserRequiredMixin, generic.UpdateView):
  template_name = 'agents/agent_update.html'
  form_class = AgentModelForm

  def get_success_url(self):
    return reverse('agents:agent_list')

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Agent.objects.filter(organisation=user.userprofile)
    return queryset


class AgentDeleteView(LoginAndOrganiserRequiredMixin, generic.DeleteView):
  template_name = 'agents/agent_delete.html'
  form_class = None

  def get_success_url(self):
    return reverse('agents:agent_list')

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Agent.objects.filter(organisation=user.userprofile)
    return queryset

