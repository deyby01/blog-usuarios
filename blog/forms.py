# Creamos un formulario usado django forms
from django import forms
from .models import Post, Comentario

# Creamos una clase que hereda de forms.ModelForm
class PostForm(forms.ModelForm):
    class Meta:
        # Modelo de donde vienen los datos o van
        model = Post
        # Solo los campos que el usuario llenara, ya que el autor, slug y demas campos se manejan automaticamente en las vistas
        fields = ['titulo', 'contenido', 'categorias',]
        
    
# ------- FORMULARIO DE COMENTARIOS ----------
class ComentarioForm(forms.ModelForm):
    class Meta:
        # Modelo de donde vienen los datos o van
        model = Comentario
        #Campos que el usuario llenara
        fields = ['contenido']
        widgets = {
            # Añadimos un widget para personalizar el campo, para que muestre en el campo el placeholder y con un espacio de 3 filas
            # hacia abajo
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aqui....'}),
        }
        labels = {
            'contenido': '' # Dejamos la etiqueta vacia.
        }
        
