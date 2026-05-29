function {:existential true} b0(c:int, limit:int, retCal:int, a17:int, a7:int, a20:int, a8:int, a12:int, a16:int, a21:int,input, i:int %Decl:i%): bool;

procedure main()
{
  var a17,a7,a20,a8,a12,a16,a21,c,limit,input,retMain,retCal,i: int;

  a17 := 1;
  a7 := 0;
  a20 := 1;
  a8 := 15;
  a12 := 8;
  a16 := 5;
  a21 := 1;

  c := 0;
  havoc limit;

  assume(%M:i%);
  	
  while (c < limit)
  invariant b0(c,limit,retCal,a17,a7,a20,a8,a12,a16,a21,input,i %Inv:i%);
  {
    assert(i > 0);

    havoc input;
    if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6))
    {
        retMain := -2;
        return;
    }

    if ((((a8 == 15) && (((((a21 == 1) && (((a16 == 5) || (a16 == 6)) && (input == 1))) && (a20 == 1)) && (a17 == 1)) && !(a7 == 1))) && (a12 == 8)))
    {
        a16 := 5;
        a20 := 0;
        retCal := 24;
    }
    else if ((((((((input == 5) && ((((a16 == 6) && (a17 == 1)) || (!(a17 == 1) && (a16 == 4))) || (!(a17 == 1) && (a16 == 5)))) && (a20 == 1)) && (a12 == 8)) && (a7 == 1)) && !(a21 == 1)) && (a8 == 13)))
    {
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
        retCal := 0;
    }
    else
    {
        retCal := -2;
    }
    
    if (retCal != 0)
    {
        c := c + 1;
    }
    i := i - 1;
  }
}
