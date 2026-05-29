function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;
  
  assume(%M:i%);
  
  while (((x >= 0 && y < 2147483647 - x) || (x < 0 && y > -2147483648 - x)) && x + y > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    if (x > 0){
      x := x - 1;
    }
    else {
      if (y > 0){
        y := y - 1;
      }
      else {
        
      }
    }
    i := i - 1;
  }
}
