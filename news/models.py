from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    ]

    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('URL', unique=True)
    content = models.TextField('Contenido')
    summary = models.TextField('Resumen', max_length=500)
    featured_image = models.ImageField('Imagen destacada', upload_to='news_images/%Y/%m/')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news_posts',
        verbose_name='Autor'
    )
    categories = models.ManyToManyField(
        NewsCategory,
        related_name='news_items',
        verbose_name='Categorías'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Estado'
    )
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    published_at = models.DateTimeField('Fecha de publicación', null=True, blank=True)

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
