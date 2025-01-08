In de eerste 'RnD' fase, hebben we elk een eigen versie van de sensormeting en de UART communicatie gemaakt om nadien te vergelijken. Maar elk van ons is daarbuiten ook andere aspecten gaan onderzoeken en uittesten.

Didah heeft onder andere het prototype ontwikkeld, de materialen verzorgd, de Pico W voorgesteld, enzovoorts.

Eva spitste zich toe op het ontwikkelen van verscheidene functies voor de kalibratie van en de uitvoering van verschillende soorten metingen, met bijbehorende UART commando's.

Michiel is dan weer uitgeweken naar implementaties van Bluetooth Low Energy (BLE) en een Pico W webserver (met een simpele webpagina). Hiervoor heeft Michiel enkele extra buffer scripts, kleine 'libraries', geschreven met bijbehorende voorbeelden.

Uiteindelijk heeft Eva dan weer gebruik gemaakt van die libraries voor BLE en Web om haar commando's en sensorfuncties ook via bluetooth en WLAN mogelijk te maken. Hiervan volgt er een extra demonstratie.

## Michiel's uitleg

[Michiel's Pico Github](https://github.com/michielkerremans/pico/tree/main/Pico) directory voor dit project.

### Tutorials

Ik volgde meerdere online [tutorials](https://github.com/michielkerremans/pico/blob/main/Pico/tutorials/pico_urls.md) waarmee ik hier enkele 'building bricks' maakte om nadien samen te kunnen metsen tot een geheel.

[Pico/tutorials/getting_started](https://github.com/michielkerremans/pico/tree/main/Pico/tutorials/getting_started)

Eerst volgde ik de 'Getting Started with Raspberry Pi Pico' tutorial, net als Eva, om zowel de programmeertaal Python te leren en de Raspberry Pi Pico W te leren kennen. Hiervoor gebruikte ik een breadboard met een drukknop, een LED en een potentiometer. En maakte ik scripts voor een ADC (met de potentiometer), een LED blinker (met de on-board LED), een externe LED blinker (met een externe LED via GPIO pinnen), een LED toggle (met de LEDs en de drukknop via GPIO pinnen), PWM (Pulse Width Modulation) en tenslotte een LED dimmer (met de potentiometer, ADC èn de PWM).

[Pico/tutorials/web_server](https://github.com/michielkerremans/pico/tree/main/Pico/tutorials/web_server)

Dan volgde ik de 'Getting started with your Raspberry Pi Pico W' om de Raspberry Pi Pico via WLAN en een webpagina te sturen. Hiervoor maakte ik enkele telkens verbeterde versies.

[Pico/tutorials/us_sensor](https://github.com/michielkerremans/pico/tree/main/Pico/tutorials/us_sensor)

Daarna gebruikte ik zowel de `picozero` library (`ultrasonic_zero.py`) als een manueel GPIO-based script (`ultrasonic_code.py`) om succesvol afstanden met de ultrasone sensor te meten.

[Pico/tutorials/bluetooth](https://github.com/michielkerremans/pico/tree/main/Pico/tutorials/bluetooth)

Nadien, testte ik BLE (Bluetooth Low Energy) communicatie, eerst met behulp van twee online scripten ([MicroPython](https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_simple_peripheral.py)) en nadien met een implementatie via de `aioble` library, met behulp van een online [tutorial](https://randomnerdtutorials.com/micropython-esp32-bluetooth-low-energy-ble/). Ook hiervoor maakte ik enkele telkens verbeterde versies.

[Pico/tutorials/uart](https://github.com/michielkerremans/pico/tree/main/Pico/tutorials/uart)

Tenslotte, testte ik de UART communicatie met een simpel polling script en Putty. Nadien kwam Eva, die dit ook had gedaan, op het idee om een **interrupt** voor de UART te gebruiken, en implementeerde zij dit met een buffer (voor de karakters), commando's en Putty. Ik heb dat dan ook uitgetest en de kleine bijdrage gedaan van de 'backspace' voor de ingave van die commando's in Putty.

### Webserver

Voor de webserver, ontwikkelde ik dus uiteindelijk een kleine [`picowlan`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picowlan.py) library met handige functies. En daarbij hoort ook een handig [`picowlan_example.py`](https://github.com/michielkerremans/pico/blob/main/Pico/examples/picowlan_example.py) voorbeeld.

### Bluetooth (BLE)

En voor de Bluetooth communicatie, ontwikkelde ik een [`picoble`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picoble.py) library met handige functies, èn een *asynchrone* werking. Met daarbij een handig [`picoble_example.py`](https://github.com/michielkerremans/pico/blob/main/Pico/examples/picoble_example.py) voorbeeld.

### Extra

In zowel de [`picowlan`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picowlan.py) library als de [`picoble`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picoble.py) library, gebruik ik functies van een derde kleine [`picoutil`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picoutil.py) library om bestanden in te lezen.

Voor de Bluetooth UUIDs, gebruik ik de [Online UUID Generator](https://www.uuidgenerator.net/), en plaats ik er drie (telkens één per lijn, één voor de service, één voor de read characteristic en één voor de write characteristic) in een `ble_uuid.txt` bestand *in het geheugen van de RPI Pico*.

Ook plaats ik voor de WLAN, een `wlan.txt` bestand *in het geheugen van de RPI Pico* met daarin de SSID op lijn 1 en het wachtwoord op lijn 2.

Tenslotte wil ik nog opmerken dat ik de `ble_write` en `ble_print` functies uit [`picoble`](https://github.com/michielkerremans/pico/blob/main/Pico/libraries/picoble.py) nog ga samensmelten tot enkel een `ble_write` (met een buffer), in de nabije toekomst.

## Eva's uitleg

Link naar [Eva's picoW Github](https://github.com/evatheunissen/picoW).

### UART

Eerst nam ik de Getting Started with Raspberry Pi Pico tutorial door. Met de bijbehorende breadboard configuratie. Daarna ging ik meteen over op het testen van een UART verbinding. Eerst via polling, dan via een interrupt. Hierbij testte ik ook zelfgemaakte commando's en responses uit via Putty.

Dan heb ik `calibrate` en `measure` functies geschreven voor de ultrasone sensor. `calibrate` kalibreert de afstand van de sensor tot de vloer. `measure` meet de afstand van de sensor tot het hoofd van de patient en trekt deze waarde af van de gekalibreerde vloerwaarde om zo de lengte van de patient te verkrijgen. Measure is inmiddels ook verbeterd met de mogelijkheid om een gemiddelde te bepalen van meerdere snelle samples, waarbij zowel het aantal samples als de toegelaten afwijking tussen de samples (t.o.v. het gemiddelde) meegegeven kunnen worden als parameters. De laatste versie van deze [`functions_lengthMeter_v2`](https://github.com/evatheunissen/picoW/blob/main/UART_3/functions_lengthMeter_v2.py) library zijn te vinden in de UART_3 folder.

Dan heb ik, in [`UART_lengthMeter.py`](https://github.com/evatheunissen/picoW/blob/main/UART_3/UART_lengthMeter.py), een UART applicatie met deze kalibratie en meting gemaakt waarbij je met commando's (via Putty) de kalibratie, een enkele meting en een meting met een zelfgekozen aantal samples en een zelfgekozen toegelaten afwijking kan starten. Bij die laatste is het zelfs mogelijk om parameters weg te laten, en *bepaalt het programma zelf* welke parameters hun standaardwaardes behouden en welke niet. Deze implementatie werkt met een interrupt, een callback en een karakterbuffer.

### WLAN / BLE

Nadien heb ik met behulp van de WLAN en BLE libraries en voorbeelden van Michiel, mijn applicatie uitgebreid met WLAN en BLE. Dit hebben we samen getest en zullen we samen demonstreren. [`picowlan_sensor.py`](https://github.com/evatheunissen/picoW/blob/main/wlan_ble/applications/picowlan_sensor.py) voor WLAN en [`picoble_sensor.py`](https://github.com/evatheunissen/picoW/blob/main/wlan_ble/applications/picoble_sensor.py) voor BLE. Bij BLE heb ik voor de gemakkelijkheid de commando's verkort tot `calib`, `meas` en `meas5` (voor 5 samples).

### Todo: POST

Voorlopig zijn we er nog niet in geslaagd om ook een POST request te versturen met de web server, om dus ook parameters mee te geven via de webpagina, maar dit gaan Michiel en ik in de toekomst samen verder uitzoeken.