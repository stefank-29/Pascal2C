int main() {
	char asd[50] = {0};
	char efg[50] = {0};
	int len;
	asd = qwerty;
	print("Unesite string: ", end="");
	readln(efg);
	writeln(Konkatenacija stringova: , asd,  + , efg);
	strcat(asd, efg)	;
	len = strlen(asd);
	writeln(Rezultat konkatenacije: , asd);
	writeln(Duzina konkatenacije: , len);
	return 0;
}