import gspread






gc = gspread.service_account(filename="clinny-361618-f313b3437739.json")
url = gc.open_by_url('https://docs.google.com/spreadsheets/d/115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')
cleaners = url.get_worksheet(0)
cleaners = cleaners.get_all_values()





url = gc.open_by_url('https://docs.google.com/spreadsheets/d/115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=480424214')