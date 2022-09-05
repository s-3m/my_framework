from datetime import date


def get_date(request):
    request['date'] = date.today().strftime("%d-%m-%Y")


fronts_list = [get_date]
