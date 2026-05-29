function {:existential true} b0(x:int, y:int, newx:int, newy:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,newx,newy,i: int;
  havoc x;
  havoc y;

  assume(%M:i%);

  while (x > 0 && y > 0)
  invariant b0(x,y,newx,newy,i %Inv:i%);
  {
    assert(i > 0);

    if (*) {

      havoc newx;
      if (newx >= x) { break; }
      x := newx;

      havoc newy;
      if (newy <= y) { break; }
      y := newy;

    } else {

      havoc newy;
      if (newy >= y) { break; }
      y := newy;

    }

    i := i - 1;
  }
}
