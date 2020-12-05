var
	n, fact, i: integer;
	x: real;
	flag: boolean;
begin
	write('Unesite pozitivan ceo broj: ');
	readln(n);
	
	fact := 1;
	x := 5.35;
	i := fact div x;
	flag := true;

	for i := 2 to n do
	begin
		fact := fact * i;
	end;
	
	writeln('Faktorijel broja ', n, ' je ', fact);
end.
