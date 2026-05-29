function {:existential true} b0(a:int, b:int, x:int, y:int %FD%): bool;

procedure main()
{
  var a,b,x,y,tmp,tmp2 %VD%: int;
  havoc a;
  havoc b;
  havoc x;
  havoc y;
  
  assume(a == b);
  %BE%
  	
  while (x >= 0 || y >= 0)
  invariant b0(a,b,x,y %IC%);
  {
    %BT%
    tmp := x + a - b - 1;
    x := y + b - a - 1;
    y := tmp;
    tmp2 := a;
    a := b;
    b := tmp2;

    %IT%
  }
}
