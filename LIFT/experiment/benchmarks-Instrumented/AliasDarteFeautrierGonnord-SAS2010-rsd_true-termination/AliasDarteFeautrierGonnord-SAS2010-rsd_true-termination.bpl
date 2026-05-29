function {:existential true} b0(_r:int, da:int, db:int, temp:int, i:int %Decl:i%): bool;

procedure main()
{
  var _r,da,db,temp,i: int;
  havoc _r;

  assume(_r >= 0);
  assume(%M:i%);

  da := 2 * _r;
  db := 2 * _r;

  while (da >= _r)
  invariant b0(_r,da,db,temp,i %Inv:i%);
  {
	assert(i > 0);
	if (*) {
		da := da - 1;
	} else {
		da := db - 1;
		db := da;
	}
	i := i - 1;
  }
}
