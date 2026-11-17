from django.shortcuts import render
from mkt.owner import OwnerCreateView, OwnerDeleteView, OwnerDetailView, OwnerListView, OwnerUpdateView
from mkt.models import Ad
# Create your views here.

class AdListView(OwnerListView):
    model = Ad

    
class AdDetailView(OwnerDetailView):
    model = Ad 


class AdCreateView(OwnerCreateView):
    model = Ad 
    fields = ['title', 'price', 'text']


class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']


class AdDeleteView(OwnerDeleteView):
    model = Ad 
    fields = ['title', 'price', 'text']
