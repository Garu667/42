#include <unistd.h>
#include <stdio.h>

void	ft_print(int i, int j, int k)
{
	char	a;
	char	b;
	char	c;

	a = i + 48;
	b = j + 48;
	c = k + 48;
	write(1, &a, 1);
	write(1, &b, 1);
	write(1, &c, 1);
	if (a == '7' && b == '8' && c == '9')
		return ;
	write(1, ", ", 2);
}

void	ft_print_comb(void)
{
	int	tab[3] = {0, 1, 2};
	while (tab[0] <= 7)
	{
		tab[1] = tab[0] + 1;
		while (tab[1] <= 8)
		{
			tab[2] = tab[1] + 1;
			while (tab[2] <= 9)
			{
				ft_print(tab[0], tab[1], tab[2]);
				tab[2]++;
			}
		tab[1]++;
		}
	tab[0]++;
	}
}
/*
int	main(void)
{
	ft_print_comb();
}
*/
