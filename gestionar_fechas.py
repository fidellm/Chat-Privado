from datetime import datetime


class Fecha:
    def __init__(self, day: str | int= None, month: str | int= None, year: str | int= None, hour: str | int= None, minute: str | int= None, second: str | int= None) -> None:
        if (
            (day == None)
            or (month == None)
            or (year == None)
            or (hour == None)
            or (minute == None)
            or (second == None)
        ):

            self._txt_fecha = self._get_time_now()
        else:
            
            self._set_txt_fecha(day, month, year, hour, minute, second)


    def _get_time_now(self): # Método para obtener la fecha y la hora actual (con mlisegundos de diferencia...)
        
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()

        # Formatear la fecha y hora actual en formato español
        fecha_hora_español = fecha_hora_actual.strftime(r"%d/%m/%Y %H:%M:%S")
        
        return fecha_hora_español

    def get_txt_fecha(self):
        return self._txt_fecha
    
    def _set_txt_fecha(self, day: int | str, month: int | str, year: int | str, hour: int | str, minute: int | str, second: int | str):
        if len(str(day)) < 2 and (not '00' in str(day) or not '0' in str(day)):
            day = '0' + str(day)
        if len(str(month)) < 2 and (not '00' in str(month) or not '0' in str(month)):
            month = '0' + str(month)
        if len(str(hour)) < 2 and (not '00' in str(hour) or not '0' in str(hour)):
            hour = '0' + str(hour)
        if len(str(minute)) < 2 and (not '00' in str(minute) or not '0' in str(minute)):
            minute = '0' + str(minute)
        if len(str(second)) < 2 and (not '00' in str(second) or not '0' in str(second)):
            second = '0' + str(second)
        
        self._txt_fecha = f'{day}/{month}/{year} {hour}:{minute}:{second}'


    def obtener_dict_fecha(self):
        # txtFecha = 'dia/mes/año horas:minutos:segundos'
        txtFecha = self._txt_fecha

        arreglo_items = txtFecha.split(' ')

        fecha = arreglo_items[0].split('/')
        tiempo = arreglo_items[1].split(':')

        day = fecha[0]
        month = fecha[1]
        year = fecha[2]

        hours = tiempo[0]
        minutes = tiempo[1]
        seconds = tiempo[2]


        return {'day': day, 'month': month, 'year': year, 'hours': hours, 'minutes': minutes, 'seconds': seconds}

    def _es_año_biciesto(self):
        year = self.obtener_dict_fecha()['year']

        return int(year) % 4 == 0
        


    def sumar_tiempo(self, sum_day: int = 0, sum_month: int = 0, sum_years: int = 0, sum_hours: int = 0, sum_minutes: int = 0, sum_seconds: int = 0):
        dict_fecha = self.obtener_dict_fecha()

        int_day = int(dict_fecha['day'])
        int_month = int(dict_fecha['month'])
        int_year = int(dict_fecha['year'])

        int_hours = int(dict_fecha['hours'])
        int_minutes = int(dict_fecha['minutes'])
        int_seconds = int(dict_fecha['seconds'])

        
        # Sumar Segundos:
        probar_minutos = sum_seconds // 60

        sum_minutes += probar_minutos
        int_seconds += ( sum_seconds - probar_minutos * 60 )


        # Sumar Minutos:
        probar_horas = sum_minutes // 60

        sum_hours += probar_horas
        int_minutes += ( sum_minutes - probar_horas * 60 )


        # Sumar Horas:
        probar_dias = sum_hours // 24

        sum_day += probar_dias
        int_hours += ( sum_hours - probar_dias * 24)


        # Sumar Días:
        meses_con_31_dias = (1, 3, 7, 8, 10, 12)

        while sum_day > 0:
            sum_day -= 1

            if int_day + 1 <= 28:
                int_day += 1
            elif int_month in meses_con_31_dias:
                if int_day + 1 <= 31:
                    int_day += 1
                else:
                    int_day = 0
                    int_month += 1
            elif int_month == 2:
                if self._es_año_biciesto():
                    if int_day + 1 <= 29:
                        int_day += 1
                    else:
                        int_month += 1
                        int_day = 0
                else:
                    if int_day + 1 <= 28:
                        int_day += 1
                    else:
                        int_month += 1
                        int_day = 0
            else:
                if int_day + 1 <= 30:
                    int_day += 1
                else:
                    int_month += 1
                    int_day = 0
        

        # Sumar Meses:
        probar_años = sum_month // 12

        sum_years += probar_años
        int_month += ( sum_month - probar_años * 12 )


        # Sumar Años:
        int_year += sum_years

        # Actualizar Fecha
        self._set_txt_fecha(int_day, int_month, int_year, int_hours, int_minutes, int_seconds)



#fecha = Fecha(27, 11, 2023, 20, 34, 0)
#fecha.sumar_tiempo(sum_day=1, sum_minutes=126)

#print(fecha.get_txt_fecha())

