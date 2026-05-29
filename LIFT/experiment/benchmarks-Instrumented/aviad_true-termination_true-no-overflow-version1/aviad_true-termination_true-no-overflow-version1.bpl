function {:existential true} b0(a:int, i:int %Decl:i%, ATTM$a_MOD_2:int, ATTM$a_MOD_3:int): bool;

procedure main()
{
  var a,i: int;
  havoc a;
  
  assume(%M:i%);
  	
  while (a > 1)
  invariant b0(a,i %Inv:i%, a mod 2, a mod 3);
  {
    assert(i > 0);
    
    if(a mod 2 == 0){
      a := a div 2;
    }
    else if(a mod 3 == 0){
        a := a div 3;
    }
    else {
      a := a + 1;
    }
    i := i - 1;
  }
}
