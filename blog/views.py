from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, ComentarioForm
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.
# Reutilizamos las clases de vistas genericas para tener un codigo mas limpio
class PostListView(ListView):
    """
    Vista para mostrar una lista de todos los post del Blog.
    """
    # Creamos la variable de paginacion para que solo muestre la cantidad de posts que le indiquemos para que no se alargue
    paginate_by = 5 # El nombre que tomara esta variable sera page_obj, que es el que usaremos en la plantilla que se renderiza.
    # Solo le pasamos el modelo de donde vienen los datos
    model = Post
    # La plantilla donde renderizar el contenido
    template_name = 'blog/post_list.html'
    # El contexto o variable que usaremos para referirnos al contenido en las plantillas
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q') # Obtenemos el parametro de busqueda 'q' de la URL
        queryset = Post.objects.filter(estado='PUBLISHED')  # Filtramos por estado 'PUBLISHED'
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | 
                Q(contenido__icontains=query)
            )
        return queryset

class PostDetailView(DetailView):
    """
    Vista para mostrar el detalle de un post especifico
    """    
    # Tambien le pasamos el modelo
    model = Post
    # La plantilla donde rederizar
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'# Nombre de la variable en la plantilla
    # DetailView buscará el objeto por su 'slug' en lugar de su 'pk' (ID)
    # gracias a que el campo 'slug' está marcado como unique=True en el modelo.
    
    def get_context_data(self, **kwargs):
        # Este metodo nos permite añadir datos extra al contexto de la plantilla.
        context = super().get_context_data(**kwargs)
        # Añadimos el formulario de comentarios al contexto
        context['comment_form'] = ComentarioForm()
        # Añadimos la lista de comentarios del post actual al contexto
        # Usamos el related_name 'comentarios' que definimos en el modelo Post
        context['comments'] = self.object.comentarios.all()
        return context
    
    def post(self, request, *args, **kwargs):
        # Este metodo se llama cuando la pagina recibe una solicitud POST.
        # Esto ocurre cuando un usuario envia el formulario de comentario.
        if not request.user.is_authenticated:
            # Por si acaso aunque escoderemos el formulario
            return redirect('login')
    
        # Obtenemos el post actual que se esta viendo
        self.object = self.get_object()
        # Creamos una instancia del formulario con los datos del POST.
        form = ComentarioForm(request.POST)
        
        if form.is_valid():
            # Si el formulario es valido creamos una instancia del modelo Comentario.
            # Pero no la guardamos todavia en la base de datos (commit=False)
            nuevo_comentario = form.save(commit=False)
            # Asignamos el post y el autor manualmente
            nuevo_comentario.post = self.object
            nuevo_comentario.autor = request.user
            # Ahora si, guardamos el comentario en la base de datos
            nuevo_comentario.save()
            # Reidirigimos al usuario a la misma pagina de detalle del post.
            # Esto sigue el patron Post/Redirect/Get para evitar reenvios del formulario
            return redirect(self.object.get_absolute_url()) # Necesitaremos definir este metodo
        else:
            # Si el formulario no es correcto volvemos a renderizar la pagina
            # con el post, los comentarios y el formulario con errores
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)
    
    
# ------------ Vistas CRUD ---------------

class PostCreateView(LoginRequiredMixin, CreateView):
    # Modelo de los datos
    model = Post
    # El formulario que va a usar
    form_class = PostForm
    # La plantilla donde se renderizara
    template_name = 'blog/post_form.html'
    # Cuando envie los datos se redirige a todos los posts
    success_url = reverse_lazy('blog:post_list') # A donde ir despues de crear
    
    # Funcion para validar datos
    def form_valid(self, form):
        # Asignamos el autor y el slug antes de guardar
        form.instance.autor = self.request.user#Se asigna el usuario de la sesion actual
        form.instance.slug = slugify(form.instance.titulo)# se pasa el titulo para que lo convierta en slug con slugfy
        # Usamos la super clase del padre para que se encargue de guardar los datos en la base de datos con el metodo form_valid
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    # Modelo de datos
    model = Post
    # Formulario a usar
    form_class = PostForm
    # Plantilla donde renderizar
    template_name = 'blog/post_form.html'
    
    # Validamos los datos
    def form_valid(self, form):
        # Atualizamos el slug si el titulo cambia
        form.instance.slug = slugify(form.instance.titulo)
        # Le pasamos los datos al metodo form_valid del padre para que los guarde en la base
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir a la pagina de detalle del post actualizado que hace referencia a la misma que se actualizo.
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo de datos
    model = Post
    # Plantilla para renderizar
    template_name = 'blog/post_confirm_delete.html'
    # Redirigimos a todos los posts
    success_url = reverse_lazy('blog:post_list')
    