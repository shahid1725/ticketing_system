# class Ticket(models.Model):
#     STATUS_CHOICES = [
#         ('OPEN', 'Open'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('RESOLVED', 'Resolved'),
#         ('CLOSED', 'Closed'),
#     ]
#
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', on_delete=models.CASCADE)
#     assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tickets', null=True, blank=True,
#                                     on_delete=models.SET_NULL)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title