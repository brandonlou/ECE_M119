#include <stdarg.h>

#define UNIT_TIME 500 // Milliseconds
#define SAME_LETTER_DELAY (1 * UNIT_TIME)
#define BETWEEN_LETTER_DELAY (3 * UNIT_TIME)
#define BETWEEN_WORD_DELAY (7 * UNIT_TIME)
#define DOT 0
#define DASH 1

const String str = "HELLO IMU";

void dot()
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(UNIT_TIME);
  digitalWrite(LED_BUILTIN, LOW);
}

void dash()
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(3 * UNIT_TIME);
  digitalWrite(LED_BUILTIN, LOW);
}

void blink(int cnt, ...)
{
  va_list args;
  va_start(args, cnt);
  for (int i = 0; i < cnt; ++i)  {
    if (va_arg(args, int) == DOT) {
      dot();
    } else {
      dash();
    }
    if (i < cnt - 1) {
      delay(SAME_LETTER_DELAY);
    }
  }
  va_end(args);  
}

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  for (unsigned int i = 0; i < str.length(); ++i) {
    const char c = str.charAt(i);
    Serial.print(c);
    switch (c) {
      case 'H':
        blink(4, DOT, DOT, DOT, DOT);
        break;
      case 'E':
        blink(1, DOT);
        break;
      case 'L':
        blink(4, DOT, DASH, DOT, DOT);
        break;
      case 'O':
        blink(3, DASH, DASH, DASH);
        break;
      case 'I':
        blink(2, DOT, DOT);
        break;
      case 'M':
        blink(2, DASH, DASH);
        break;
      case 'U':
        blink(3, DOT, DOT, DASH);
        break;
      default:
        break;
    }

    if (c == ' ') {
      delay(BETWEEN_WORD_DELAY);
    } else if (i < str.length() - 1 && str.charAt(i + 1) != ' ') {
      delay(BETWEEN_LETTER_DELAY);
    }

  }

  Serial.println("");
  delay(BETWEEN_WORD_DELAY);
}
