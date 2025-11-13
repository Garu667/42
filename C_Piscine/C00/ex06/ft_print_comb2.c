#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_print(int i, int j)
{
	ft_putchar((i / 10) + 48);
	ft_putchar((i % 10) + 48);
	ft_putchar(32);
	ft_putchar((j / 10) + 48);
	ft_putchar((j % 10) + 48);
	if (i == 98 && j == 99)
		return ;
	ft_putchar(',');
	ft_putchar(32);
}

void	ft_print_comb2(void)
{
	int	tab[2] = {0, 1};
	while (tab[0] <= 98)
	{
		tab[1] = tab[0] + 1;
		while (tab[1] <= 99)
		{
			ft_print(tab[0], tab[1]);
			tab[1]++;
		}
		tab[0]++;
	}
}
/*
int	main(void)
{
	ft_print_comb2();
}
*/
