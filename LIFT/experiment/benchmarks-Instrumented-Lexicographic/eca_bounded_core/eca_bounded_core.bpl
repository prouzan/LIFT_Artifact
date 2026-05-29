function {:existential true} b0(c:int, limit:int, retCal:int, a17:int, a7:int, a20:int, a8:int, a12:int, a16:int, a21:int,input %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int, TR6:int, TR7:int): bool;

procedure main()
{
  var a17,a7,a20,a8,a12,a16,a21,c,limit,input,retMain,retCal %VD%, TR1, TR2, TR3, TR4, TR5, TR6, TR7: int;

  a17 := 1;
  a7 := 0;
  a20 := 1;
  a8 := 15;
  a12 := 8;
  a16 := 5;
  a21 := 1;

  c := 0;
  havoc limit;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;
  	
  while (c < limit)
  invariant b0(c,limit,retCal,a17,a7,a20,a8,a12,a16,a21,input %IC%, TR1, TR2, TR3, TR4, TR5, TR6, TR7);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;

    havoc input;
    if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6))
    {
TR1 := 1;
        retMain := -2;
        return;
    }

    if ((((a8 == 15) && (((((a21 == 1) && (((a16 == 5) || (a16 == 6)) && (input == 1))) && (a20 == 1)) && (a17 == 1)) && !(a7 == 1))) && (a12 == 8)))
    {
TR2 := 1;
        a16 := 5;
        a20 := 0;
        retCal := 24;
    }
    else if ((((((((input == 5) && ((((a16 == 6) && (a17 == 1)) || (!(a17 == 1) && (a16 == 4))) || (!(a17 == 1) && (a16 == 5)))) && (a20 == 1)) && (a12 == 8)) && (a7 == 1)) && !(a21 == 1)) && (a8 == 13)))
    {
TR3 := 1;
        a20 := 0;
        a16 := 6;
        a17 := 0;
        a8 := 15;
        a7 := 0;
        a21 := 1;
        retCal := 26;
    }
    else if (((a12 == 8) && ((input == 1) && (((a21 == 1) && (((a8 == 15) && ((!(a17 == 1) && !(a7 == 1)) && !(a20 == 1))) && (a16 == 6))) || (!(a21 == 1) && ((a16 == 4) && ((a8 == 13) && (((a17 == 1) && (a7 == 1)) && (a20 == 1)))))))))
    {
TR4 := 1;
        a7 := 1;
        a17 := 1;
        a21 := 0;
        a20 := 1;
        a8 := 13;
        a16 := 5;
        retCal := 26;
    }
    else if (((((((!(a17 == 1) && !(a7 == 1)) && (a20 == 1)) && (a8 == 13)) && (a12 == 8)) && (a16 == 5)) && (a21 == 1)))
    {
TR5 := 1;
        retCal := 0;
    }
    else
    {
TR6 := 1;
        retCal := -2;
    }
    
    if (retCal != 0)
    {
TR7 := 1;
        c := c + 1;
    }
    %IT%
  }
}
