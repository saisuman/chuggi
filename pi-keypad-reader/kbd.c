#include <wiringPi.h>
#include <stdio.h>

// How frequently we scan the columns.
#define MATRIX_SCAN_HIGH_DURATION_MICROS 900
// How long we hold the 'HIGH' level for a column.
#define MATRIX_SCAN_PAUSE_DURATION_MICROS 100
// The number of columns in the keypad matrix.
#define NUM_COLS 3
// The number of rows in the keypad matrix.
#define NUM_ROWS 4

// The WiringPI pin numbers for the column outputs.
const int COL_PINS[] = {0, 1, 2};
// The WiringPI pin numbers for the row inputs.
const int ROW_PINS[] = {3, 4, 5, 6};

// A mapping from (row, column) to the keypad
// character each location represents.
const char MATRIX_MAPPING[NUM_ROWS][NUM_COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

// Stores the last known states of each key in the
// keypad matrix.
int keystate[NUM_ROWS][NUM_COLS] = {{0}, {0}, {0}, {0}};

// Sets up the pin modes.
void setupPins() {
  wiringPiSetup();  // WiringPi layout.
  // We'll use the column pins for output, and
  // the row pins for input.
  int i;
  for (i = 0; i < NUM_COLS; ++i) {
    pinMode(COL_PINS[i], OUTPUT);
  }

  // The output pins also need to have their
  // pull-up register mode activated.
  for (i = 0; i < NUM_ROWS; ++i) {
    int curr_pin = ROW_PINS[i];
    pinMode(curr_pin, INPUT);
    pullUpDnControl(curr_pin, PUD_DOWN);  // Pull down on all inputs.
  }
}

// Scans all the rows in the specific column and updates
// any key states that have changed since the last scan of 
// this column.
void updateKeyStates(int curr_col_pin_index) {
  int i;
  for (i = 0; i < NUM_ROWS; ++i) {
    int curr_state = digitalRead(ROW_PINS[i]) == HIGH ? 1 : 0;
    int old_state = keystate[i][curr_col_pin_index];
    if (curr_state == old_state) {
      continue;
    }
    keystate[i][curr_col_pin_index] = curr_state;
    char key = MATRIX_MAPPING[i][curr_col_pin_index];
    printf("%s:%c\n", curr_state == 0 ? "KEYUP" : "KEYDOWN", key);
  }
}

// Continuously scans the keypad matrix for key state changes.
// If this hogs too much CPU, simply reduce the frequency at which
// it scans each column.
void loop() {
  int curr_col_pin_index = 0;
  while(1) {
    int curr_col_pin = COL_PINS[curr_col_pin_index];
    digitalWrite(curr_col_pin, HIGH);
    updateKeyStates(curr_col_pin_index);
    delayMicroseconds(MATRIX_SCAN_HIGH_DURATION_MICROS);
    digitalWrite(curr_col_pin, LOW);
    delayMicroseconds(MATRIX_SCAN_PAUSE_DURATION_MICROS);
    ++curr_col_pin_index;
    curr_col_pin_index = curr_col_pin_index > NUM_COLS - 1 ? 0 : curr_col_pin_index;
  }
}

int main(int argc, char **argv) {
  setupPins();
  loop();
  return 0;
}

