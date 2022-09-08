import gspread

gc = gspread.service_account(filename="clinny-361618-f313b3437739.json")
calc_sheet_url = gc.open_by_url('https://docs.google.com/spreadsheets/d/'
                                '115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')


def get_extra_services_data():
    return calc_sheet_url.get_worksheet(4).get_all_values()


def get_basic_service_data():
    return calc_sheet_url.get_worksheet(5).get_all_values()


def get_base_clean_info():
    clean_info = calc_sheet_url.get_worksheet(1).get_all_values()
    clean_zones = []
    clean_zones_description = []
    for i in clean_info:
        clean_zones.append(i[0])
        clean_zones_description.append(i[1])

    return clean_zones, clean_zones_description


def get_cleaners_info():
    cleaners_info = calc_sheet_url.get_worksheet(0).get_all_values()[1:]
    names = []
    photos = []
    experiences = []
    descriptions = []
    for i in cleaners_info:
        names.append(i[0])
        photos.append(i[1])
        experiences.append(i[2])
        descriptions.append(i[3])

    return cleaners_info
