from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from mkt.owner import OwnerCreateView, OwnerDeleteView, OwnerDetailView, OwnerListView, OwnerUpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from mkt.models import Ad, Comment
from mkt.forms import CreateForm, CommentForm
# Create your views here.

class AdListView(OwnerListView):
    model = Ad

    
class AdDetailView(OwnerDetailView):
    model = Ad 
    template_name = 'mkt/ad_detail.html'


    def get(self, request, pk):
        ad =  get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        ctx = { 'ad': ad, 'comment_list' : comments, 'comment_form': comment_form}
        return render(request, self.template_name, ctx)


class AdCreateView(LoginRequiredMixin, View ):
    template_name = 'mkt/ad_form.html'
    success_url = reverse_lazy('mkt:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)
        print(form)
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(OwnerUpdateView):
    template_name = 'mkt/ad_form.html'
    success_url = reverse_lazy('mkt:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)
        if not form.is_valid():
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad 
    fields = ['title', 'price', 'text']

def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response 


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad =get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse_lazy('mkt:ad_detail', args=[ad.id])) 

class CommentDeleteView(OwnerDeleteView):
    model = Comment


    def get_success_url(self):
        ad = self.object.ad
        return reverse_lazy('mkt:ad_detail', args=[ad.id])