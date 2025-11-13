#include <unistd.h>
#include <stdio.h>
#define N 10

int	ft_nqueens(int tab[N][N])
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (i < N)
	{
		if (search_queens(tab, N, i, j))
	}
	return 0;
}

int	main(void)
{
	printf("%d\n", N);
}
