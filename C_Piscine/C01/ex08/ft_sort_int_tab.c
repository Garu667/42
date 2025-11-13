#include <stdio.h>

void	ft_sort_int_tab(int *tab, int size)
{
	int	i = 0;
	int	j = 0;
	int	tmp = 0;

	while (i < size)
	{
		j = 0;
		while (j < size)
		{
			if (tab[j] > tab[i])
			{
				tmp = tab[j];
				tab[j] = tab[i];
				tab[i] = tmp;
			}
		j++;
		}
	i++;
	}
}

/*
int	main(void)
{
	int	tab[] = {3, 2, 1, 4, 8, 9};
	int	i = 0;

	ft_sort_int_tab(tab, 6);
	while (i < 6)
	{
		printf("%d\n", tab[i]);
		i++;
	}
}
*/
