from datetime import datetime


class Fecha:
    def __init__(self, day: str | int= None, month: str | int= None, year: str | int= None, hours: str | int= None, minutes: str | int= None, seconds: str | int= None) -> None:
        if (
            (day == None)
            or (month == None)
            or (year == None)
            or (hours == None)
            or (minutes == None)
            or (seconds == None)
        ):

            self._txt_fecha = self._get_time_now()
        else:
            
            self.set_txt_fecha(day, month, year, hours, minutes, seconds)


    def _get_time_now(self) -> str: # Método para obtener la fecha y la hora actual (con mlisegundos de diferencia...)
        
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()

        # Formatear la fecha y hora actual en formato español
        fecha_hora_español = fecha_hora_actual.strftime(r"%d/%m/%Y %H:%M:%S")
        
        return fecha_hora_español

    def get_txt_fecha(self) -> str:
        return self._txt_fecha
    
    def set_txt_fecha(self, day: int | str, month: int | str, year: int | str, hour: int | str, minutes: int | str, seconds: int | str):
        if len(str(day)) < 2 and (not '00' == str(day) or not '0' in str(day)):
            day = '0' + str(day)
        if len(str(month)) < 2 and (not '00' == str(month) or not '0' in str(month)):
            month = '0' + str(month)
        if len(str(hour)) < 2 and (not '00' == str(hour) or not '0' in str(hour)):
            hour = '0' + str(hour)
        if len(str(minute)) < 2 and (not '00' == str(minute) or not '0' in str(minute)):
            minute = '0' + str(minute)
        if len(str(second)) < 2 and (not '00' == str(second) or not '0' in str(second)):
            second = '0' + str(second)
        
        self._txt_fecha = f'{day}/{month}/{year} {hour}:{minute}:{second}'


    def get_dict_fecha(self) -> dict['day': str, 'month': str, 'year': str, 'hours': str, 'minutes': str, 'seconds': str]:
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
    
    def set_dict_fecha(self, new_dict_fecha: dict['day': str, 'month': str, 'year': str, 'hours': str, 'minutes': str, 'seconds': str]) -> None:
        self.set_txt_fecha(day= new_dict_fecha['day'], month= new_dict_fecha['month'], 
                           year= new_dict_fecha['year'], hours= new_dict_fecha['hour'], 
                           minutes= new_dict_fecha['minutes'], seconds= new_dict_fecha['seconds'])

    def _es_año_biciesto(self) -> bool:
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
        
    def mayor_que(self, fecha2, mute_years: bool= False, mute_months: bool= False, mute_days: bool= False, mute_hours: bool= False, mute_minutes: bool= False, mute_seconds: bool= False) -> bool:
        dict_fecha1 = self.get_dict_fecha().copy()
        dict_fecha2 = fecha2.get_dict_fecha().copy()
        
        if mute_seconds:
            dict_fecha1['seconds'] = '00'
            dict_fecha2['seconds'] = '00'
        if mute_minutes:
            dict_fecha1['minutes'] = '00'
            dict_fecha2['minutes'] = '00'
        if mute_hours:
            dict_fecha1['hours'] = '00'
            dict_fecha2['hours'] = '00'
        if mute_days:
            dict_fecha1['day'] = '00'
            dict_fecha2['day'] = '00'
        if mute_months:
            dict_fecha1['month'] = '00'
            dict_fecha2['month'] = '00'
        if mute_years:
            dict_fecha1['year'] = '0000'
            dict_fecha2['year'] = '0000'
        
        
        if dict_fecha1['year'] == dict_fecha2['year']:
            pass
        elif int(dict_fecha1['year']) > int(dict_fecha2['year']):
            return True
        
        
        if dict_fecha1['month'] == dict_fecha2['month']:
            pass
        elif int(dict_fecha1['month']) > int(dict_fecha2['month']):
            return True
        
        
        if dict_fecha1['day'] == dict_fecha2['day']:
            pass
        elif int(dict_fecha1['day']) > int(dict_fecha2['day']):
            return True
        
        
        if dict_fecha1['hours'] == dict_fecha2['hours']:
            pass
        elif int(dict_fecha1['hours']) > int(dict_fecha2['hours']):
            return True
        
        
        if dict_fecha1['minutes'] == dict_fecha2['minutes']:
            pass
        elif int(dict_fecha1['minutes']) > int(dict_fecha2['minutes']):
            return True
        
        
        if int(dict_fecha1['seconds']) > int(dict_fecha2['seconds']):
            return True
        
        
        return False


    def menor_que(self, fecha2, mute_years: bool= False, mute_months: bool= False, mute_days: bool= False, mute_hours: bool= False, mute_minutes: bool= False, mute_seconds: bool= False) -> bool:
        dict_fecha1 = self.get_dict_fecha().copy()
        dict_fecha2 = fecha2.get_dict_fecha().copy()
        
        if mute_seconds:
            dict_fecha1['seconds'] = '00'
            dict_fecha2['seconds'] = '00'
        if mute_minutes:
            dict_fecha1['minutes'] = '00'
            dict_fecha2['minutes'] = '00'
        if mute_hours:
            dict_fecha1['hours'] = '00'
            dict_fecha2['hours'] = '00'
        if mute_days:
            dict_fecha1['day'] = '00'
            dict_fecha2['day'] = '00'
        if mute_months:
            dict_fecha1['month'] = '00'
            dict_fecha2['month'] = '00'
        if mute_years:
            dict_fecha1['year'] = '0000'
            dict_fecha2['year'] = '0000'
        
        
        if dict_fecha1['year'] == dict_fecha2['year']:
            pass
        elif int(dict_fecha1['year']) < int(dict_fecha2['year']):
            return True
        
        
        if dict_fecha1['month'] == dict_fecha2['month']:
            pass
        elif int(dict_fecha1['month']) < int(dict_fecha2['month']):
            return True
        
        
        if dict_fecha1['day'] == dict_fecha2['day']:
            pass
        elif int(dict_fecha1['day']) < int(dict_fecha2['day']):
            return True
        
        
        if dict_fecha1['hours'] == dict_fecha2['hours']:
            pass
        elif int(dict_fecha1['hours']) < int(dict_fecha2['hours']):
            return True
        
        
        if dict_fecha1['minutes'] == dict_fecha2['minutes']:
            pass
        elif int(dict_fecha1['minutes']) < int(dict_fecha2['minutes']):
            return True
        
        
        if int(dict_fecha1['seconds']) < int(dict_fecha2['seconds']):
            return True
        
        
        return False
    
    
    def equals(self, fecha2, mute_seconds: bool= False, mute_minutes: bool= False, mute_hours: bool= False, mute_days: bool= False, mute_months: bool= False, mute_years: bool= False) -> bool:
        dict_fecha1 = self.get_dict_fecha().copy()
        dict_fecha2 = fecha2.get_dict_fecha().copy()
        
        if mute_seconds:
            dict_fecha1['seconds'] = '00'
            dict_fecha2['seconds'] = '00'
        if mute_minutes:
            dict_fecha1['minutes'] = '00'
            dict_fecha2['minutes'] = '00'
        if mute_hours:
            dict_fecha1['hours'] = '00'
            dict_fecha2['hours'] = '00'
        if mute_days:
            dict_fecha1['day'] = '00'
            dict_fecha2['day'] = '00'
        if mute_months:
            dict_fecha1['month'] = '00'
            dict_fecha2['month'] = '00'
        if mute_years:
            dict_fecha1['year'] = '0000'
            dict_fecha2['year'] = '0000'
            
        
        return dict_fecha1 == dict_fecha2
    
    def diferencia(self, fecha2, type_return: str= 'int' | 'float' | 'str' | 'Fecha()', diferencia_en: str= 'seconds' | 'minutes' | 'hours' | 'days' | 'months' | 'years') -> int | float | str:
        dict_fecha1 = self.get_dict_fecha()
        dict_fecha2 = fecha2.get_dict_fecha()
        
        if diferencia_en == 'seconds':
            dict_fecha1['minutes'] == '00'
            dict_fecha1['hours'] == '00'
            dict_fecha1['day'] == '00'
            dict_fecha1['month'] == '00'
            dict_fecha1['year'] == '00'
            
            dict_fecha1['minutes'] == '00'
            dict_fecha2['hours'] == '00'
            dict_fecha2['day'] == '00'
            dict_fecha2['month'] == '00'
            dict_fecha2['year'] == '00'
        
        if diferencia_en == 'minutes':
            dict_fecha1['seconds'] == '00'
            dict_fecha1['hours'] == '00'
            dict_fecha1['day'] == '00'
            dict_fecha1['month'] == '00'
            dict_fecha1['year'] == '00'
            
            dict_fecha2['seconds'] == '00'
            dict_fecha2['hours'] == '00'
            dict_fecha2['day'] == '00'
            dict_fecha2['month'] == '00'
            dict_fecha2['year'] == '00'
            
        if diferencia_en == 'hours':
            dict_fecha1['seconds'] == '00'
            dict_fecha1['minutes'] == '00'
            dict_fecha1['day'] == '00'
            dict_fecha1['month'] == '00'
            dict_fecha1['year'] == '00'
            
            dict_fecha2['seconds'] == '00'
            dict_fecha2['minutes'] == '00'
            dict_fecha2['day'] == '00'
            dict_fecha2['month'] == '00'
            dict_fecha2['year'] == '00'
            
        if diferencia_en == 'days':
            dict_fecha1['seconds'] == '00'
            dict_fecha1['minutes'] == '00'
            dict_fecha1['hours'] == '00'
            dict_fecha1['month'] == '00'
            dict_fecha1['year'] == '00'
            
            dict_fecha2['seconds'] == '00'
            dict_fecha2['minutes'] == '00'
            dict_fecha2['hours'] == '00'
            dict_fecha2['month'] == '00'
            dict_fecha2['year'] == '00'
            
        if diferencia_en == 'years':
            dict_fecha1['seconds'] == '00'
            dict_fecha1['minutes'] == '00'
            dict_fecha1['hours'] == '00'
            dict_fecha1['day'] == '00'
            dict_fecha1['month'] == '00'
            
            dict_fecha2['seconds'] == '00'
            dict_fecha2['minutes'] == '00'
            dict_fecha2['hours'] == '00'
            dict_fecha2['day'] == '00'
            dict_fecha2['month'] == '00'
        
        
        fecha2_segundos = int(dict_fecha2['seconds'])
        fecha1_segundos = int(dict_fecha1['seconds'])
        
        ## Metodo no terminado...
        


fecha = Fecha(27, 11, 2024, 0, 10, 0)
fecha2 = Fecha(27, 11, 2024, 0, 0, 0)

print(fecha.get_dict_fecha())
print(fecha2.get_dict_fecha())
es_igual = fecha.equals(fecha2)

print(es_igual)


#fecha.sumar_tiempo(sum_day=1, sum_minutes=126)

#print(fecha.get_txt_fecha())

