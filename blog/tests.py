from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Categoria

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.categoria = Categoria.objects.create(nombre='Django')
        self.client.login(username='testuser', password='12345')

    def test_crear_post(self):
        post = Post.objects.create(
            titulo='Mi primer post',
            slug='mi-primer-post',
            autor=self.user,
            contenido='Contenido de prueba',
            estado='PUBLISHED',
        )
        post.categorias.add(self.categoria)
        self.assertEqual(post.titulo, 'Mi primer post')
        self.assertEqual(post.autor.username, 'testuser')
        self.assertIn(self.categoria, post.categorias.all())
    
    # vamos a crear una prueba para verificar si la pagina de los posts tiene un formulario de busqueda
    def test_pagina_tiene_formulario_busqueda(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'Buscar')
        
    # Crear una prueba que prepare posts, simule una busqueta y verifique que los resultados son correctos
    def test_busqueda_posts(self):
        post1 = Post.objects.create(
            titulo='Info Django',
            slug='info-django',
            autor=self.user,
            contenido='Contenido de prueba 1',
            estado='PUBLISHED',
        )
        post2 = Post.objects.create(
            titulo='Info Git',
            slug='info-git',
            autor=self.user,
            contenido='Contenido de prueba 2',
            estado='PUBLISHED',
        )
        response = self.client.get(reverse('blog:post_list'), {'q': 'Django'})
        self.assertContains(response, post1.titulo)
        self.assertNotContains(response, post2.titulo)

class CategoriaTest(TestCase):
    def test_crear_categoria(self):
        categoria = Categoria.objects.create(nombre='Python')
        self.assertEqual(categoria.nombre, 'Python')

    def test_categoria_str(self):
        categoria = Categoria.objects.create(nombre='JavaScript')
        self.assertEqual(str(categoria), 'JavaScript')
        
