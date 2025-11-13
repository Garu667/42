#include <unistd.h>

int	ft_atoi(char *str)
{
	int	number;
	int	sign;

	sign = 1;
	number = 0;
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (*str == '-' || *str == '+')
	{
		if (*str == '-')
			sign = -1;
		str++;
	}
	while (*str >= '0' && *str <= '9')
	{
		number = number * 10 + (*str - 48);
		str++;
	}
	return (number * sign);
}

void	ft_combn(int n, int current_n, int start, int *tab)
{
	int		i;
	char	c;

	i = 0;
	if (current_n == n) // Si on a une combinaison complète
	{
		while (i < n) // Print la combinaison de chiffre complète
		{
			c = tab[i] + 48;
			write(1, &c, 1);
			i++;
		}
		if (tab[0] != (10 - n)) // Si la combinaison n'est pas la dernière
			write(1, ", ", 2);
		return ;
	}
	i = start;
	while (i <= (10 - (n - current_n))) // Construit le tableau avec la combinaison actuel
	{
		tab[current_n] = i;
		ft_combn(n, current_n + 1, i + 1, tab);
		i++;
	}
}

void	ft_print_combn(int n)
{
	int	tab[n];

	ft_combn(n, 0, 0, tab);
}
/*
int	main(int ac, char **av)
{
	int	n;

	if (ac != 2 || !(ft_atoi(av[1]) >= 1 && ft_atoi(av[1]) <= 9))
	{
		write(1, "Donner un nombre entre 1 et 9\n", 30);
		return (0);
	}
	n = ft_atoi(av[1]);
	ft_print_combn(n);
}
*/
