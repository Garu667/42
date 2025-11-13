#include <stdlib.h>
#include <stdio.h>

int	ft_ultimate_range(int **range, int min, int max)
{
	int i;

	i = 0;
	if (min >= max)
	{
		*range = malloc(sizeof(int *));
		range[0] = NULL;
		return (0);
	}
	range[0] = malloc((max - min) * sizeof(int));
	while (min < max)
	{
		range[0][i] = min;
		i++;
		min++;
	}
	return (i);
}
/*
int	main(void)
{
	int **range;
	int i = 0;
	printf("%d\n", ft_ultimate_range(range, 0, 0));
	while (i != 6)
	{
		printf("%d\t", range);
		i++;
	}
}
*/
