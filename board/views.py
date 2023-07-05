import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView

from board.forms import AddAnnouncementForm, CommentCreateForm
from board.models import Announcement, Category, Comment
from board.tasks import ann_created
from board.utils import DataMixin
from django.contrib import messages


class PostList(ListView):
    model = Announcement
    template_name = 'announcement/list.html'
    context_object_name = 'announcements'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostCategory(DataMixin, ListView):
    model = Announcement
    template_name = 'announcement/list.html'
    context_object_name = 'announcements'
    paginate_by = 4

    def get_queryset(self):
        """
        Убираем два лишних запроса к БД за счет select_related.
        """
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Announcement.objects.filter(category=self.category).select_related('category')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetail(DetailView):
    model = Announcement
    template_name = 'announcement/detail.html'

    def get_success_url(self):
        return reverse('announcement_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category
        context['announcement'] = Announcement.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(announcement=context['announcement'], active=True)
        return context


class AnnouncementCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Создание нового объявления.
    """
    permission_required = 'news.add_post'
    form_class = AddAnnouncementForm
    model = Announcement
    template_name = 'announcement/announcement_create.html'

    def form_valid(self, form):
        """
        ann_created - таска на отправку уведомления всем зарегистрированным пользователям о создании нового объявления.
        """
        post = form.save(commit=False)
        if self.request.method == 'POST':
            post.author, created = User.objects.get_or_create(id=self.request.user.id)
            post.save()
            messages.success(self.request, 'Объявление успешно создано')
        else:
            messages.error(self.request, 'Произошла ошибка, пожалуйста повторите действие или обратитесь к администратору')
            ann_created(announcement_id=post.id)
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AnnouncementUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Announcement
    form_class = AddAnnouncementForm
    template_name = 'announcement/announcement_update.html'
    context_object_name = 'announcement'
    success_message = "Объявление отредактировано успешно!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        """
        Если зарегистрированный пользователь является автором - позволяем редактирование объявления, иначе - статус 403.
        """
        post = self.get_object()
        if post.author == self.request.user:
            self.template_name = 'announcement/announcement_update.html'
            return self.template_name
        else:
            raise PermissionDenied


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'announcement/comment_create.html'
    form_class = CommentCreateForm
    success_url = '/success/'

    def form_valid(self, form):
        """
        Создаем отклик и отправляем автору объявления письмо о новом отклике.
        """
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.announcement = Announcement.objects.get(id=self.kwargs['pk'])
        self.object.save()
        result = super().form_valid(form)
        send_mail(
            subject=f'Получен отклик по объявлению "{self.object.announcement.title}"',
            message=f'Получен новый отклик по вашему объявлению: "{self.object.text}"',
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=[self.object.announcement.author.email]
        )
        messages.success(self.request, 'Ваш отклик успешно отправлен!')
        return result


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment

    def get_template_names(self):
        response = self.get_object()
        if response.announcement.author == self.request.user:
            self.template_name = 'announcement/comment_detail.html'
            return self.template_name
        else:
            raise PermissionDenied


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'announcement/comment_list.html'
    context_object_name = 'comment_list'
    ordering = '-created'

    def get_queryset(self):
        queryset = Comment.objects.filter(announcement__author=self.request.user)
        return queryset


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'announcement/success.html'


@login_required()
def accept_comment(request, pk):
    """
    Отправляем пользователю уведомление по почте, чот его отклик принят.
    """
    comment = Comment.objects.get(pk=pk)
    comment.active = True
    recipient_email = comment.announcement.author.email
    comment.save()
    send_mail(
        subject=f'Доска объявлений: отклик принят',
        message=f'Ваш отклик на пост "{comment.announcement.title}" принят',
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        recipient_list=[recipient_email]
    )
    messages.success(request, 'Отклик принят!')
    return HttpResponseRedirect(reverse('board:comment_list'))


@login_required()
def deny_comment(request, pk):
    """
    При нажатии кнопки 'отклонить' - убираем отображение отклика со страницы с объявлением.
    Реализовано вместо функции удаления, чтобы оставлять отклики в БД, просто меняя их статус.
    """
    comment = Comment.objects.get(pk=pk)
    comment.active = False
    comment.save()
    messages.success(request, 'Отклик отклонен!')
    return HttpResponseRedirect(reverse('board:comment_list'))
