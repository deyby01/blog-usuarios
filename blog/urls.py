from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

# Siempre es bueno definir el namespace para no tener colisiones de nombres con otras apps
app_name = 'blog' # Definimos el namespace

urlpatterns = [
    # URL para todos los posts
    path('', PostListView.as_view(), name='post_list'),
    # Para crear un nuevo post
    path('post/nuevo/', PostCreateView.as_view(), name='post_create'),
    # URL para detalle le dira a django que use una url dinamica tipo slug, ya que usara el slug del post.
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    # Usa el slug seleccionado para editar
    path('<slug:slug>/editar/', PostUpdateView.as_view(), name='post_edit'),
    # Usa el slug seleccionado para eliminar
    path('<slug:slug>/eliminar/', PostDeleteView.as_view(), name='post_delete'),
]
