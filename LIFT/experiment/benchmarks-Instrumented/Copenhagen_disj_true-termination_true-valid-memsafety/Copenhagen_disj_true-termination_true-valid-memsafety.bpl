function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,oldx,i: int;
  havoc x;
  havoc y;
  
  assume(-1073741823 <= x && x <= 1073741823);
  assume(-1073741823 <= y && y <= 1073741823);
  assume(%M:i%);
  	
  while (x >= 0 || y >= 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    oldx := x;
    x := y - 1;
    y := oldx - 1;

    i := i - 1;
  }
}
