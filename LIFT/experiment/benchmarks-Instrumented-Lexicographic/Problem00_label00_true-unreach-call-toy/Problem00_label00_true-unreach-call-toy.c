#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
    return rand();
}

int a7 = 0;


int main() {
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    // default output
    int output = -1;

    a7 = 0;

    // main i/o-loop
    while(output != 0)
    {
        printf("#\n");
        // read input
        int input = _nondet_int();
        if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6)) {
printf("L1\n");return -2;}

        // operate eca engine
        a7++;
        if (a7 == 10) {
printf("L2\n"); output = 0; } else {
printf("L3\n"); output = input - 1; }
        // output = calculate_output(input);
    }
}
