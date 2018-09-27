from time import sleep
from pyrfidhid import RfidHid

def main():
    """Main Read Tag Function"""

    try:
        # Try to open RFID device using default vid:pid (ffff:0035)
        rfid = RfidHid()
    except Exception as e:
        print(e)
        exit()

    # Initialize device
    print('Initializing device...')
    rfid.init()
    sleep(0.02)
    print('Done!')
    print ('Please hold a tag to the reader until you hear a beep...\n')

    id_temp = None

    while True:
        payload_response = rfid.read_tag()
        if payload_response.has_id_data():
            uid = payload_response.get_tag_uid()
            # Avoid processing the same tag (CID/UID) more than once in a row
            if uid != id_temp:
                id_temp = uid
                print('uid: %s' % uid)
                print('customer_id: %s' % payload_response.get_tag_cid())
                print('CRC Sum: %s' % hex(payload_response.get_crc_sum()))
                w26 = payload_response.get_tag_w26()
                if w26:
                    print('W26: facility code = %d, card number = %d' % w26)
                print('')
                rfid.beep()
        else:
            id_temp = None
        sleep(0.1)


if __name__ == "__main__": 
    main()