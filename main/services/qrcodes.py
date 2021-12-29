from PIL import Image

from pyzbar.pyzbar import decode

from main.clients import FNSClient
from main.models import Ticket, Item


class QRService:

    def __init__(self):
        self.client = FNSClient()
        print(self.client)

    def process_photo(self, file_name: str) -> None:
        img = Image.open(file_name)
        data = decode(img)[0].data
        ticket_dict = self.client.get_ticket(qr=data.decode('utf-8'))
        ticket = Ticket(data=ticket_dict)
        ticket.save()
        items = ticket_dict['ticket']['document']['receipt']['items']
        Item.objects.bulk_create([Item(name=item.get('name'),
                                       paymentType=item.get('paymentType'),
                                       price=item.get('price')/100,
                                       quantity=item.get('quantity'),
                                       sum=item.get('sum')/100,
                                       ticket=ticket) for item in items])
