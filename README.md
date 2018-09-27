# RaspberryPi-Sicaklik-Kontrol
This python application uses raspberry pi, python, ds18b20 and 4ch relay switch to cool down or heat a water tank. Application is Turkish for now. 
When you launch the app, it asks you 2 questions: 1. Minimum Temperature in Celcius and 2. Maximum temperature in Celcius.
After that app measures temperature every 60 seconds. If temperature goes down to below minimum temperature, relay switch turns on water heater resistant and water circular pump. Water heater resistant heats water, circulation pump circulates that water inside tank and heats the liquid until temperature interval that user designated in begining.
If temperature increase to maximum temperature than, relay switch turns on peltier cooling device and circulation pump.
