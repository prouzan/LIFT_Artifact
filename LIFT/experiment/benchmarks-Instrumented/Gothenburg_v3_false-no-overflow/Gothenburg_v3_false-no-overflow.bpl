function {:existential true} b0(a:int, b:int, x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var a,b,x,y,tmp,i: int;
  havoc a;
  havoc b;
  havoc x;
  havoc y;
  
  assume(a == b);
  assume(%M:i%);
  	
  while (x >= 0 || y >= 0)
  invariant b0(a,b,x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := x + a - b - 1;
    y := y + b - a - 1;
    tmp := a;
    a := b;
    b := tmp;

    i := i - 1;
  }
}
