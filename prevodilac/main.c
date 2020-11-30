int main() {
	int n, i, j;
	char space, star;
	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", n);
	space = ' ';
	star = '*';
	for (i = 1; i <= n; i = i + 1) {
		for (j = 1; j <= n - i; j = j + 1) {
			printf("%c", space);
		}
		for (j = 1; j <= 2 * i + 1; j = j + 1) {
			printf("%c", star);
		}
		printf("\n");
	}
	return 0;
}