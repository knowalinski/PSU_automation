# Automatyzacja pracy zasilacza HMP4040

## Cel zadania:
Przystosowanie zasilacza HMP4040 z kartą rozszerzeń z interfejsami USB/RS232 do zdalnego sterowania z więcej niż jednego stanowiska.

## Wymagane funkcjonalności:
1. Możliwość załączenia zadanego zasilania na wybranym kanale bez dodatkowej ingerencji z wykorzystaniem CANoe.
2. Możliwość sterowania przez GUI.

### **Określenie możliwości sterowania zasilaczem.**

W tym celu stworzony został zestaw skryptów, których celem było przetestowanie wybranych metod przekazywania poleceń standardu [SCPI](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments) z poziomu Pythona. Testowane biblioteki to [PyVisa](https://pyvisa.readthedocs.io/en/latest/) oraz [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html). Obie w powierzonym zadaniu poradziły sobie podobnie.

Wnioski:
+ PyVisa jako biblioteka dedykowana do pracy z ze standardem SCPI wydaje się bardzo dobrym rozwiązaniem, jednak ze względu na to, że przeznaczona jest do niszowych protokołów komunikacyjnych ma słabe wsparcie społeczności

+ pySerial to biblioteka często stosowana przez hobbystów do komunikacji na linii mikrokontroler - PC, z tego powodu zdecydowanie łatwiej znaleźć poradniki oraz rozwiązania konkretnych problemów występujących przy pracy.

*Ze względu na powyższe zalety oraz na wcześniejsze doświadczenie została wybrana biblioteka pySerial.*

### **Określenie ograniczeń w sterowaniu**
Po określeniu możliwości sterowania, należało sprawdzić ograniczenia. Na początku został określony zestaw komend jakie będą potrzebne do efektywnej pracy z zasilaczem. Poniżej stosowane w dalszej pracy komendy ze standardu SCPI:

**Ustawienie stanu wyjścia zasilacza:**

    OUTP:GEN {state}

**Wybór kanału zasilacza:**

    INST:NSEL {channel_id}

**Ustawienie stanu wyjścia aktualnie wybranego kanału:**

    OUTP:SEL {state}

**Ustawienie parametrów wyjścia aktualnie wybranego kanału:**

    APPL {voltage}, {current}

Określeny zestawu poleceń został na początku wykorzystany do napisanie skryptu, którego celem było możliwie jak największe obciążenie sterownika portu szeregowego w zasilaczu.

Poniżej najprostsza forma skryptu, która zmusza zasilacz do jak naszybszego ustawiania wartości napięcia na kanale:
```python
while True:
    for i in range(31):
        serial.write(f"APPL {i}, 1\n".encode())
```
Zgodnie z oczekiwaniami każda próba kończyła się timeoutem zasilacza. Dodanie opóźnień w wykonaniu kodu odkładało występowanie błędu w czasie. Problemem też okazało się zbyt długie otwarcie portu szeregowego, dlatego finalna wersja przesyłania wiadomości została zaimplementowana jako dekorator:
```python
    def _serial_handler(body):
        def wrapper(self, *arg, **kw):
            self.serial_id.open()
            time.sleep(.015)
            body(self, *arg, **kw)
            time.sleep(.015)
            self.serial_id.close()
```
Jak widać, na początku następuje otwarcie portu szeregowego. Niewielkie opóźnienie gwarantuje, że podczas przesłania informacji port będzie otwarty. Po wysłaniu komendy następuje kolejne opóźnienie - zapobiegające zamknięciu portu przed zakończeniem odbierania wiadomości przez zasilacz.

### **Dostępność z poziomu wielu urządzeń - serwer**
Aby umożliwić dostęp do zasilacza z poziomu wielu urządzeń stworzona została hostowana w sieci lokalnej usługa.

Część serwerowa została stworzony przy pomocy frameworka [Flask](https://flask.palletsprojects.com/en/2.2.0/). Obsługuje konwersje zapytań do poleceń wysyłanych do zasilacza oraz renderowanie interfejsu webowego. Sam serwer WSGI został postawiony przy pomocy [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/).

### **Dostępność z poziomu wielu urządzeń - klient**
Klient działa na zasadzie generowania zapytań wysyłanych na serwer usługi. Zapytania generowane są na podstawie zawartości pliku. Zawartość jest tworzona przez skrypt aktywowany przy starcie i zakończeniu pomiarów w programie CANoe.

# **poniżej rzeczy, które są w trakcie**
### **Dostępność z poziomu wielu urządzeń - interfejs**
Interfejs programu renderowany przez serwer jest dostępny z poziomu dowolnej przeglądarki internetowej. Został stworzony przy pomocy html/css
