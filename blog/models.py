from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Opciones para el nuevo campo
CHOICES = [('DRAFT','Borrador'),
           ('PUBLISHED','Publicado'),]

# Modelo para las categorias de los posts
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre  

# Create your models here.
class Post(models.Model):
    # CharField para textos cortos, max para 200 caracteres como max, unique para que no se repitan los titulos.
    titulo = models.CharField(max_length=200, unique=True)
    # SlugField para crear el slug para la url en vez de pk, tambien corto y unico.
    slug = models.SlugField(max_length=200, unique=True)
    # ForeignKey establece relacion con el usurio, y models.CASCADE indica que si un usuario se elimina tambien
    # sus posts, 'blog_post' nos permite acceder a los post de un usuario desde su objeto usuario haciendo mas facil obtenerlo.
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # TextField permite campos de bastante contenido
    contenido = models.TextField()
    # Auto_now_add indica que se asigna fecha al momento de crear un objeto post
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # auto_now actualiza la fecha si se modifica el objeto
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Nuevo campo para publicar el post o dejarlo en borrador
    estado = models.CharField(max_length=100, choices=CHOICES, default='DRAFT')
    categorias = models.ManyToManyField(Categoria, related_name='posts')
    
    # Metadatos
    class Meta:
        # Ordena los posts por fecha de creacion, del mas nuevo al mas antiguo
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.titulo
    
    #----- Nuevo Metodo ------
    def get_absolute_url(self):
        """Devuelve la URL para acceder a una instancia particular de un post."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
# Modelo que usaremos para almacenar los comentarios
class Comentario(models.Model):
    # Es la relacion, cada comentario esta relacionado a un post, CASCADE, si se elimina un post se eliminan todos su comentarios
    # related_name='comentarios' nos permite acceder a todos los comentarios de un post a travez del objeto post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    # Relacionamos el comentario con el autor que lo escribio
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    # Un textField para el contenido ya que almacena bastante información
    contenido = models.TextField()
    # Fecha de creacion se almacena automaticamente al crear un comentari u objeto comentario
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Mostramos del mas antiguo al mas nuevo
        ordering = ['fecha_creacion']
    
    # Una representacion del objeto
    # OJO, esto solo se mostrara en el panel de admin/
    def __str__(self):
        return f'Comentario de {self.autor} en {self.post}'
    

