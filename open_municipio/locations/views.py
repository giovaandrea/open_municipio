from django.views.generic import DetailView, FormView
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from open_municipio.acts.models import Act

from open_municipio.locations.models import Location
from open_municipio.locations.forms import ActLocationsAddForm


class LocationDetailView(DetailView):
    context_object_name = 'location'
    template_name = 'taxonomy/location_detail.html'
    model = Location


class ActTagByLocationView(FormView):
    form_class = ActLocationsAddForm
    
    # FIXME: restrict access to editor users    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ActTagByLocationView, self).dispatch(*args, **kwargs)
    
    def get_object(self):
        act = get_object_or_404(Act, pk=self.kwargs['pk'])
        return act
    
    def form_valid(self, form):
        self.act.location_set = form.cleaned_data['locations']
        return HttpResponseRedirect(self.get_success_url())
       
    def form_invalid(self, form=None):
        msg = "It appears that the monitoring form has been tampered with !"
        return HttpResponseBadRequest(msg)
    
    def get_success_url(self):
        return self.act.downcast().get_absolute_url()
    
    def post(self, request, *args, **kwargs):
        self.act = self.get_object()
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)