from ..models.library_models import *


def get_member_by_id(member_id):
	try:
		member = Members.objects.get(id=member_id)
	except:
		member = None
	return member


def get_books_by_id(book_id):
	try:
		book = Books.objects.get(id=book_id)
	except:
		book = None

	return book


def get_checkout_by_id(checkout_id):
	try:
		checkout = CheckOut.objects.get(id=checkout_id)
	except:
		checkout = None
	return checkout