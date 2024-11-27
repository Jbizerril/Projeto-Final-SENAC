from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import csv
from .models import Event, Inscription
from .forms import InscriptionForm
from django.db.models import Count

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            inscription = form.save(commit=False)
            inscription.event = event
            inscription.save()
            return redirect('event_detail', pk=pk)
    else:
        form = InscriptionForm()
    return render(request, 'events/event_detail.html', {'event': event, 'form': form})

def edit_inscription(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    if request.method == "POST":
        form = InscriptionForm(request.POST, instance=inscription)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=inscription.event.id)
    else:
        form = InscriptionForm(instance=inscription)
    return render(request, 'events/edit_inscription.html', {'form': form, 'event_pk': inscription.event.id})

def cancel_inscription(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    event_id = inscription.event.id
    inscription.delete()
    return redirect('event_detail', pk=event_id)

def inscription_report(request):
    events = Event.objects.annotate(inscription_count=Count('inscription'))
    return render(request, 'events/inscription_report.html', {'events': events})

def export_inscriptions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inscriptions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Event', 'Participant Name', 'Email', 'Date Registered'])
    inscriptions = Inscription.objects.all()
    for inscription in inscriptions:
        writer.writerow([inscription.event.name, inscription.participant_name, inscription.email, inscription.date_registered])
    
    return response