# your_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1) HOME (landing) view
    path("", views.home, name="home"),

    # Detail page: scrollable text + notes area
    path('textsumm/<int:pk>/', views.view_text, name='view_text'),

    # AJAX endpoints for notes:
    path('textsumm/<int:textsumm_id>/save_note/', views.save_note, name='save_note'),
    path('notes/<int:note_id>/', views.get_note, name='get_note'),
    path('notes/<int:note_id>/edit/', views.edit_note,   name='edit_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)