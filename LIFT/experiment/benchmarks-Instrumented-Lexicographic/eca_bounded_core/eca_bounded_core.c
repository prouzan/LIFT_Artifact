#include <stdio.h>
#include <stdlib.h>
int _nondet_7(void)
{
    return rand() % 7;
}

int a17 = 1;
int a7 = 0;
int a20 = 1;
int a8 = 15;
int a12 = 8;
int a16 = 5;
int a21 = 1;

int main()
{
    int c = 0;
    int limit;
    int retCal;
    scanf("%d", &limit);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (c < limit)
    {
        printf("%d\n", limit);

        int input = _nondet_7();
        if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6))
        {
printf("L1\n");
            return -2;
        }

        if ((((a8 == 15) && (((((a21 == 1) && (((a16 == 5) || (a16 == 6)) && (input == 1))) && (a20 == 1)) && (a17 == 1)) && !(a7 == 1))) && (a12 == 8)))
        {
printf("L2\n");
            a16 = 5;
            a20 = 0;
            retCal = 24;
        }
        else if ((((((((input == 5) && ((((a16 == 6) && (a17 == 1)) || (!(a17 == 1) && (a16 == 4))) || (!(a17 == 1) && (a16 == 5)))) && (a20 == 1)) && (a12 == 8)) && (a7 == 1)) && !(a21 == 1)) && (a8 == 13)))
        {
printf("L3\n");
            a20 = 0;
            a16 = 6;
            a17 = 0;
            a8 = 15;
            a7 = 0;
            a21 = 1;
            retCal = 26;
        }
        else if (((a12 == 8) && ((input == 1) && (((a21 == 1) && (((a8 == 15) && ((!(a17 == 1) && !(a7 == 1)) && !(a20 == 1))) && (a16 == 6))) || (!(a21 == 1) && ((a16 == 4) && ((a8 == 13) && (((a17 == 1) && (a7 == 1)) && (a20 == 1)))))))))
        {
printf("L4\n");
            a7 = 1;
            a17 = 1;
            a21 = 0;
            a20 = 1;
            a8 = 13;
            a16 = 5;
            retCal = 26;
        }
        else if (((((((!(a17 == 1) && !(a7 == 1)) && (a20 == 1)) && (a8 == 13)) && (a12 == 8)) && (a16 == 5)) && (a21 == 1)))
        {
printf("L5\n");
            retCal = 0;
        }
        else {
printf("L6\n");retCal = -2;}

        if (retCal != 0)
            {
printf("L7\n");c++;}
    }
}
