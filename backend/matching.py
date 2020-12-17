import backend.sql as SQ

def match(vtrPhone, vtrZip):
    
    phonesandzips = SQ.get_requester_phones_and_zips()
    info = []
    for (phone,zipcode) in phonesandzips:
        if vtrZip == zipcode:
            info = SQ.get_requester_info(phone)
            break
    return info


