#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
}

String read_serial()
{
  String str = "";

  while (Serial.available())
  {
    str = Serial.readString();
    delay(10);
  }

  return str;
}

void loop()
{
  String str = read_serial();

  if (str == "1")
  {
    lcd.clear();
  }
  else
  {
    // Assuming str is in the format "temp,humid"
    int commaIndex = str.indexOf(',');
    if (commaIndex != -1)
    {
      String temp_str = str.substring(0, commaIndex);
      String humid_str = str.substring(commaIndex + 1);

      float temp = temp_str.toFloat();
      float humid = humid_str.toFloat();

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(temp);
      lcd.print(" C");

      lcd.setCursor(0, 1);
      lcd.print("Humid: ");
      lcd.print(humid);
      lcd.print(" %");
    }
  }
}
