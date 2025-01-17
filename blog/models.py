from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User  # Blog author or commenter
from django.utils import timezone


class BlogAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="Enter your bio details here.")
    image = models.ImageField(default='anon.png', upload_to='profile_pics')

    class Meta:
        ordering = ["user", "bio"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog-author instance.
        """
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Rewrite save method to check and resize images
        """
        from PIL import Image
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Blog(models.Model):
    """
    Model representing a blog post.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateTimeField(default=timezone.now)
    # post_date = models.DateField(default=date.today)

    # Foreign Key used because Blog can only have one author/User, but bloggsers can have multiple blog posts.
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class BlogComment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    text = models.TextField(max_length=100, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.text) > len_title:
            titlestring = self.text[:len_title] + '...'
        else:
            titlestring = self.text
        return titlestring
