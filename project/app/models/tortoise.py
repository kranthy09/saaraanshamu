"""
Models for application
"""

from tortoise import fields, models


class TextSummary(models.Model):
    """Text summary for a url"""

    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class AppUser(models.Model):
    """User model for application"""

    username = fields.TextField()
    hashed_password = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# class Card(models.Model):
#     """Card to store knowledgeble information"""

#     title = fields.TextField()
#     content = fields.TextField()
#     created_at = fields.DatetimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
