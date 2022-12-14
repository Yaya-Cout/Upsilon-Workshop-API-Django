"""Database models for the Upsilon Workshop app."""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Import the User and Group models from the Django auth module
from django.contrib.auth.models import User, Group

# Import the validators from the validators.py file
from workshop.api.validators import validate_language, validate_email, validate_script_files

# Max file size is 100 KB
MAX_FILE_SIZE = 100 * 1024

# Configure user to make email required
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('email').validators = [validate_email]


class Rating(models.Model):
    """Model for the rating of a script."""

    # The rating is a number between 0 and 5
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    # The comment is an optional text field that can be used to explain the
    # rating
    comment = models.TextField(blank=True)

    # The created and modified fields are automatically set by Django
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # The user that created the rating
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    # The script that was rated
    script = models.ForeignKey(
        'Script',
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return str(self.rating)


class OS(models.Model):
    """Operating system model."""

    # The name of the operating system
    name = models.CharField(max_length=100)

    # The description of the operating system
    description = models.TextField(blank=True)

    # The URL of the operating system
    url = models.URLField(blank=True)

    # TODO: Add a version field
    # TODO: Add a icon field

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.name}"


class Script(models.Model):
    """A script stored in the database.

    Scripts are stored in the database as a string of text.
    They have metadata associated with them:
    - The name of the script
    - The author of the script
    - The date the script was created
    - The date the script was last modified
    - The language the script is written in
    - The version of the script
    - The description of the script
    - The comments on the script
    - The number of times the script has been downloaded
    - The number of times the script has been viewed
    - The content of the script
    - The licence of the script
    - The compatibility of the script
    - and more...
    """

    # The files that are used in the script
    files = models.JSONField(
        validators=[validate_script_files]
    )

    # The name of the script
    # TODO: Forbid multiple scripts with the same name for the same user, but
    # allow multiple scripts with the same name for different users
    name = models.CharField(max_length=100)

    # The author of the script (user is keept when the script is deleted,
    # but the script is deleted when the user is deleted)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='scripts'
    )

    # The date the script was created
    created = models.DateTimeField(auto_now_add=True)

    # The date the script was last modified
    modified = models.DateTimeField(auto_now=True)

    # The language the script is written in (listed in
    # ALLOWED_LANGUAGES in validators.py)
    language = models.CharField(max_length=100, validators=[validate_language])

    # The version of the script
    version = models.CharField(max_length=100, default='1.0')

    # The description of the script
    description = models.TextField(blank=True)

    # The number of times the script has been downloaded
    # downloads = models.IntegerField(default=0)

    # The number of times the script has been viewed
    views = models.IntegerField(default=0)

    # The licence of the script
    licence = models.CharField(max_length=100, default='MIT')

    # The compatibility of the script
    # TODO: Forbid empty values
    compatibility = models.ManyToManyField(OS, blank=True)

    # TODO: Add a field for the tags of the script
    # TODO: Add a field for compatibles machines
    # TODO: Add a field for size of the script
