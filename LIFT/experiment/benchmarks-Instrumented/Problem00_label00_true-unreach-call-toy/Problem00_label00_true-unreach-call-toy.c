#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
    return rand();
}

int a7 = 0;


int main() {
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    // default output
    int output = -1, input;

    a7 = 0;

    // main i/o-loop
    while(output != 0)
    {
        printf("a7:%d,output:%d,input:%d\n", a7, output, input);
        // read input
        input = _nondet_int();
        if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6)) {return -2;}

        // operate eca engine
        a7++;
        if (a7 == 10) { output = 0; } else { output = input - 1; }
        // output = calculate_output(input);
    }
}
