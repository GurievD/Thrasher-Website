from django.views import generic
from .models import Album, Song, Comment, Review, ReviewComment
from newsapi import NewsApiClient 
from django.shortcuts import render 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from bs4 import BeautifulSoup
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import requests
import urllib 
import re

requests.packages.urllib3.disable_warnings()

class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            all_albums = Album.objects.filter(Q(album_title__icontains=search_query) | Q(genre__icontains=search_query) | Q(artist__icontains=search_query))
        else:
            all_albums = Album.objects.all()
        
        return all_albums

    

class ConditionView(generic.DetailView):
    model = Album
    template_name = 'music/condition.html'


class MainpageView(generic.ListView):
    template_name = 'music/mainpage.html'
    def get_queryset(self):
        pass


class AlbumCreate(CreateView):
    template_name = 'music/album_form.html'

    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
    template_name = 'music/album_form.html'

    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    template_name = 'music/album_form.html'
    model = Album
    success_url = reverse_lazy('index')

class PostCreate(CreateView):
    template_name = 'music/album_form.html'
    model = Comment
    fields = ['text', 'created_date', 'approved_comment']
    def form_valid(self, form):
        comment = get_object_or_404(Album, pk=self.kwargs['pk'])
        form.instance.post = comment
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)
        

class PostUpdate(UpdateView):
    template_name = 'music/album_form.html'

    model = Comment
    fields = ['text', 'created_date', 'approved_comment']

class PostDelete(DeleteView):
    template_name = 'music/album_form.html'
    model = Comment

    def get_success_url(self):
        comment = self.object.post 
        return reverse_lazy('param', kwargs={'pk': comment.id})

class SongCreate(CreateView):
    template_name = 'music/album_form.html'

    model = Song
    fields = ['file_type', 'song_title', 'audiotrack', 'is_favorite']

    def form_valid(self, form):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        form.instance.album = album
        return super(SongCreate, self).form_valid(form)

class SongUpdate(UpdateView):
    template_name = 'music/album_form.html'

    model = Song
    fields = ['file_type', 'song_title', 'audiotrack', 'is_favorite']


class SongDelete(DeleteView):
    template_name = 'music/album_form.html'
    model = Song

    def get_success_url(self):
        album = self.object.album 
        return reverse_lazy('param', kwargs={'pk': album.id})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'
    def get(self, request):
        form = self.form_class(request.POST or None)
        return render(request, 'music/registration_form.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.is_staff = True
            user.set_password(password)
            user.save()

            user = authenticate(user=username, password=password)

            if user is not None:
                if user.is_staff:
                    login(request, user)
            return redirect('index')

        return render(request, self.template_name, {'form': form})


def get_summary(url):
    new_d = BeautifulSoup(requests.get(url).text, 'html.parser')
    return '\n'.join(i.text for i in new_d.find('div', {'class':'flexible_content_wrap'}).find_all('p')) 

def scrape(request):
    website_url = requests.get("https://rockcult.ru/news/").text
    sessions = requests.Session()
    sessions.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    soup = BeautifulSoup(website_url, "html.parser")

    articles = []
    excarr = []
    img = []
    mysrcset = []
    more = []

    links = soup.find_all('h2', {'class': None})
    excerpt = soup.find_all('div', {'class': 'excerpt'})
    myimg = soup.find_all('img', {'class': 'attachment-rc_post_thumbnail size-rc_post_thumbnail wp-post-image'})
    teaser = soup.find_all('div', {'class':'teaser_feed_common'})
    
    for image in myimg:
        img.append(image.get('src'))
        srcset = image.get('srcset')
        mysrcset.append(image.get('srcset'))
        print(srcset)

    for l in links:
        print(l.text)
        articles.append(l.text)
    
    for e in excerpt:
        print(e.text)
        excarr.append(e.text)
    
    for i in teaser:
        mine = get_summary(i.a['href'])
        print(mine)
        more.append(mine)

    mylist = zip(articles, excarr, more, img, mysrcset)
    context = {'list': mylist}
    return render(request, 'music/news.html', context)




class ReviewIndexView(generic.ListView):
    template_name = 'music/review.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            all_albums = Review.objects.filter(Q(review_title__icontains=search_query) | Q(review_artist__icontains=search_query))
        else:
            all_albums = Review.objects.all()
        
        return all_albums

class ReviewConditionView(generic.DetailView):
    model = Review
    template_name = 'music/revparam.html'



class ReviewCreate(CreateView):
    template_name = 'music/album_form.html'

    model = Review
    fields = ['review_artist', 'review_title', 'review_logo', 'review_text', 'review_grade']
    success_url = reverse_lazy('revindex')
    def form_valid(self, form):
        form.instance.review_author = self.request.user
        return super(ReviewCreate, self).form_valid(form)

class ReviewUpdate(UpdateView):
    template_name = 'music/album_form.html'

    model = Review
    fields = ['review_artist', 'review_title', 'review_logo', 'review_text', 'review_grade']
    success_url = reverse_lazy('revindex')

class ReviewDelete(DeleteView):
    template_name = 'music/album_form.html'
    model = Review
    success_url = reverse_lazy('revindex')




class ReviewPostCreate(CreateView):
    template_name = 'music/album_form.html'
    model = ReviewComment
    fields = ['text', 'created_date', 'approved_comment']
    def form_valid(self, form):
        comment = get_object_or_404(Review, pk=self.kwargs['pk'])
        form.instance.post = comment
        form.instance.author = self.request.user
        return super(ReviewPostCreate, self).form_valid(form)
        
class ReviewPostUpdate(UpdateView):
    template_name = 'music/album_form.html'

    model = ReviewComment
    fields = ['text', 'created_date', 'approved_comment']

class ReviewPostDelete(DeleteView):
    template_name = 'music/album_form.html'
    model = ReviewComment

    def get_success_url(self):
        comment = self.object.post 
        return reverse_lazy('revparam', kwargs={'pk': comment.id})

