#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int ft_atoi(char *str)
{
	int	sign;
	int	number;

	sign = 0;
	number = 0;
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	while (*str == '-' || *str == '+')
	{
		if (*str == '-')
			sign++;
		str++;
	}
	while (*str >= '0' && *str <= '9')
	{
		number = number * 10 + (*str - 48);
		str++;
	}
	if (sign % 2 == 1)
		return (-number);
	return (number);
}
/*
int	ft_atoi(char *str)
{
	int	sign;
	int	number;

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


int	main(int ac, char **av)
{
	if (ac != 2)
	{
		printf("%s number\n", av[0]);
		return (0);
	}
	printf("\nft_atoi: %d\n", ft_atoi(av[1]));
	printf("atoi: %d\n", atoi(av[1]));
}
*/
