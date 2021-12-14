from server.main.clients import FNSClient

if __name__ == '__main__':
    client = FNSClient()
    qr_code = "t=20211211T000300&s=344.97&fn=9960440300738941&i=28144&fp=3622676507&n=1"
    ticket = client.get_ticket(qr_code)
    from pprint import pprint
    pprint(ticket['ticket']['document']['receipt']['items'])

