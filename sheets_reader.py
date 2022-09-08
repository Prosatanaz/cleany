import gspread


gc = gspread.service_account(filename="clinny-361618-f313b3437739.json")
calc_sheet_url = gc.open_by_url('https://docs.google.com/spreadsheets/d/'
                                '115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')


def get_extra_services_data():
    return calc_sheet_url.get_worksheet(4).get_all_values()


def get_basic_service_data():
    return calc_sheet_url.get_worksheet(5).get_all_values()
