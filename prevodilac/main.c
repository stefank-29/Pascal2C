int main() {
	int n, i, j, temp;
	int niz[100];
	printf("Unesite pozitivan ceo broj: ");
	scanf("%d", n);
	for (i = 1; i <= n; i = i + 1) {
		printf("Unesite ceo broj za %d. element niza: ", i);
		scanf("%d", niz[i]);
	}
	for (i = 1; i <= n; i = i + 1) {
		for (j = i + 1; j <= n; j = j + 1) {
			if (niz[i] > niz[j]) {
				temp = niz[i];
				niz[i] = niz[j];
				niz[j] = temp;
			}
		}
	}
	printf("Sortirani niz: ");
	for (i = 1; i <= n; i = i + 1) {
		printf("");
		if (i == n) {
			printf("\n");
		}
		else  {
			printf(" ");
		}
	}
	return 0;
}