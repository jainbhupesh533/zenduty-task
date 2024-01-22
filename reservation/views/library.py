from django.db.models import Count, Avg, F
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reservation.constants import FINE_VALUE
from reservation.models import *
from reservation.serializers.library import *
from reservation.utils.create_reservation import *



class BooksApiView(APIView):

    def get(self, request):
        book_id = request.query_params.get('book_id', None)
        if not book_id:
            return Response({'error': "Pass the book id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Books.objects.get(id=book_id)
        except:
            book = None

        serializer = BooksSerializer(book).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.get('book_data', None)
        if not data:
            return Response({'error': "Pass the book data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BooksInputSerializer(data = data, many=True)
        if serializer.is_valid():
            books_data = serializer.save()
            return Response({'status':True}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueBooksApiView(APIView):

    def get(self, request):
        member_id = request.query_params.get('member_id', None)
        if not member_id:
            return Response({'error': "Pass the member data"}, status=status.HTTP_400_BAD_REQUEST)
        today = timezone.now()
        checkout_data = CheckOut.objects.filter(reservation__member_id=member_id, due_date__gte=today)
        serializers = CheckOutSerializer(checkout_data, many=True).data
        return Response(serializers, status=status.HTTP_200_OK)

    def post(self, request):
        reservation_data = request.data.get('data', None)
        if not reservation_data:
            return Response({'error': "Pass the reservation data"}, status=status.HTTP_400_BAD_REQUEST)
        checkout_created_data = []
        reservation_created_data = []
        for data in reservation_data:
            option_type = data.get('type', None)
            member_id = data.get('member_id', None)
            book_id = data.get('book_id', None)
            reservation = create_reservation_for_member(member_id, book_id)
            if reservation is None:
                pass
            if option_type == 'checkout':
                checkout_data = create_checkout_for_book(reservation)
                if checkout_data.get('status'):
                    serializers = CheckOutSerializer(checkout_data.get('data')).data
                    checkout_created_data.append(serializers)
                else:
                    checkout_created_data.append(checkout_data)
            else:
                serializers = ReservataionSerializer(reservation).data
                reservation_created_data.append(serializers)
        data = {
            'reservation_data': reservation_created_data,
            'checkout_data': checkout_created_data,
            'status': True

        }
        return Response(data, status=status.HTTP_201_CREATED)


class MemberDuesAPiView(APIView):

    def get(self, request):
        member_id = request.query_params.get('member_id', None)
        if not member_id:
            return Response({'error': "Pass the member data"}, status=status.HTTP_400_BAD_REQUEST)
        member = get_member_by_id(member_id)
        if not member:
            return Response({'error': "member not found"}, status=status.HTTP_400_BAD_REQUEST)
        today = timezone.now()
        data = []
        checkout_data = CheckOut.objects.prefetch_related('reservation').filter(reservation__member=member,
                                                                                due_date__lte=today,
                                                                                returned_date__isnull=True)
        for data in checkout_data:
            due_date = checkout_data.due_date
            days = (today - due_date).days
            data.append({
                'total_fine': days * FINE_VALUE,
                'book_name': checkout_data.reservation.book.name,
                'due_date': due_date
            })
        return Response(data, status=status.HTTP_200_OK)


class ReturnBookApiView(APIView):

    def get(self, request):
        checkout_id = request.query_params.get('checkout_id', None)
        if not checkout_id:
            return Response({'error': "Pass the checkout data"}, status=status.HTTP_400_BAD_REQUEST)
        data = return_book(checkout_id)
        return Response(data, status=status.HTTP_202_ACCEPTED)


class AnalyticsView(APIView):

    def get(self, request, *args, **kwargs):
        most_popular_books = Books.objects.annotate(num_checkouts=Count('reservationqueue__checkout')).order_by('-num_checkouts')[:5]
        avg_duration = CheckOut.objects.filter(checked_out=True).aggregate(avg_duration=Avg(F('due_date') - F('reserved_date')))
        most_active_members = Members.objects.annotate(num_checkouts=Count('reservationqueue__checkout')).order_by('-num_checkouts')[:5]
        book_serializer = BookCheckoutsSerializer(most_popular_books, many=True)
        member_serializer = MemberCheckoutSerializer(most_active_members, many=True)

        data = {
            'most_popular_books': book_serializer.data,
            'average_checkout_duration': avg_duration['avg_duration'],
            'most_active_members': member_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)