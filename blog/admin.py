from django.contrib import admin
from .models import Post, Comentario, Categoria

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    # Como su nombre lo indica, solo para lectura para no tener problemas al ejecutar
    readonly_fields = ('fecha_creacion',)
    # estas columnas se mostraran en el admin
    list_display = ('titulo', 'slug', 'autor', 'fecha_creacion', 'estado')
    # Filtro al lado derecho para buscar pos fecha o autor
    list_filter = ('fecha_creacion', 'autor')
    # Barra de busqueda por titulo o contenido
    search_fields = ['titulo', 'contenido']
    # Esta linea es la magia para autocompletar el slug, a medida que se escribe el titulo.
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ('categorias',)

# Registramos el modelo en admin para poder visualizarlo en /admin
admin.site.register(Post, PostAdmin)

@admin.register(Comentario)# Esta es otra forma de registrar con un decorador lo que hace que sea mas limpio y pyhtonico
class ComentarioAdmin(admin.ModelAdmin):
    # Asignamos la fecha de creacion solo para lectura para no tener errores en ejecucion, para que django sepa que esta columna se
    # crea automaticamente.
    readonly_fields = ('fecha_creacion',)
    # Las columnas que se mostraran en el admin
    list_display = ('autor', 'contenido', 'post', 'fecha_creacion')
    # Un panel de filtrado
    list_filter = ('fecha_creacion', 'autor')
    # Barra de busqueda por autor y contenido
    # como autor es una ForeignKey para buscar el objeto relacionado user usamos la sintaxis de __ bajo
    search_fields = ['autor__username', 'contenido']
    
admin.site.register(Categoria)