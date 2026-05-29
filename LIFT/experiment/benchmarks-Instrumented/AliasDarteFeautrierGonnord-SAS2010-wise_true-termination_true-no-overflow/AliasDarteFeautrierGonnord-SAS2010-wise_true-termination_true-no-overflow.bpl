function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x$SUB$y:int, ATTM$y$SUB$x:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;
  
  assume(x >= 0 && y >= 0);
  assume(%M:i%);
  	
  while (x - y > 2 || y - x > 2)
  invariant b0(x,y,i %Inv:i%, x-y, y-x);
  {
    assert(i > 0);
    if(x < y){
      x := x + 1;
    }
    else {
      y := y + 1;
    }
    i := i - 1;
  }
}
