from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from ..models.library_models import *
from .library import *


def create_reservation_for_member(member_id, book_id):
	member = get_member_by_id(member_id)
	book = get_books_by_id(book_id)
	if not (member and book):
		return None

	try:
		with transaction.atomic():
			query_data = {
				'book': book,
				'member': member,
			}
			now = timezone.now()
			existing_reservation = ReservationQueue.objects.filter(book=book, member=member, created_at__gte=now,
			                                                       created_at__lte=now + timedelta(days=7)).first()
			if existing_reservation:
				return existing_reservation
			reservation_count = ReservationQueue.objects.filter(book=book, reserved=True).count()
			query_data['queue_order'] = reservation_count + 1
			reservation = ReservationQueue.objects.create(**query_data)
			return reservation
	except:
		return None


def create_checkout_for_book(reservation):
	if not reservation.book.available_copies > 0:
		return {'error': 'cant checkout as books is not available', 'status': False}
	try:
		with (transaction.atomic()):
			reservation.queue_order = 0
			reservation.reserved = True
			book = reservation.book
			book.available_copies -= 1
			book.save()
			reservation.save()
			due_date = (timezone.now() + timedelta(days=7))
			checkout = CheckOut.objects.create(reservation=reservation, due_date=due_date, checked_out=True)
			return {'data': checkout, 'status': True}
	except Exception as e:
		return {'error': e, 'status': False}


def return_book(checkout_id):
	try:
		checkout_data = CheckOut.objects.prefetch_related('reservation__book').get(id=checkout_id)
	except:
		return {'error': "checkout data not found"}
	today = timezone.now()
	try:
		with transaction.atomic():
			reservation = checkout_data.reservation
			reservation.reserved = False
			checkout_data.returned_date = today
			checkout_data.checked_out=False
			book = reservation.book
			book.available_copies += 1
			book.save()
			reservation.save()
			checkout_data.save()
			new_reservation = ReservationQueue.objects.filter(book=book, reserved=False, queue_order__gt=0).order_by(
				'-queue_order').first()
			if new_reservation:
				create_checkout_for_book(new_reservation)
				all_reservations = ReservationQueue.objects.filter(book=book, reserved=False, queue_order__gt=0).order_by(
					'-queue_order')
				if all_reservations:
					all_reservations.update(queue_order=models.F('queue_order') - 1)
			return {'status': True}
	except Exception as e:
		return {'error': e}