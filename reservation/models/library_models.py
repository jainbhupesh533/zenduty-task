from django.db import models
from ..models.user import User


# Create your models here.
class Author(models.Model):
	name = models.CharField(max_length= 50, db_index=True)

	def __str__(self):
		return self.name


class Books(models.Model):
	name = models.CharField(max_length=50, db_index=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, db_index=True)
	available_copies = models.PositiveIntegerField(default=0)


class Members(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.name


class ReservationQueue(models.Model):
	book = models.ForeignKey(Books, on_delete=models.CASCADE)
	member = models.ForeignKey(Members, on_delete=models.CASCADE)
	queue_order = models.PositiveIntegerField(default=0, db_index=True)
	reserved = models.BooleanField(default=False, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.member} - {self.book}'


class CheckOut(models.Model):
	reservation = models.ForeignKey(ReservationQueue, on_delete=models.CASCADE)
	reserved_date = models.DateTimeField(auto_now_add=True, db_index=True)
	due_date = models.DateTimeField(null=True, blank=True, db_index=True)
	checked_out = models.BooleanField(default=False)
	returned_date = models.DateTimeField(null=True, blank=True, db_index=True)