#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int	check_base(char *base)
{
	int	i;
	int	j;

	i = 0;
	if (base[0] == '\0' || base[1] == '\0')
		return (-1);
	while (base[i])
	{
		j = 0;
		while (base[j])
		{
			if (i != j && base[i] == base[j])
				return (-1);
			j++;
		}
		i++;
	}
	return (i);
}

int	is_in_base(char c, char *base)
{
	int	i;

	i = 0;
	while (base[i])
	{
		if (c == base[i])
			return (i + 1);
		i++;
	}
	return (0);
}

int	power(int num, int power)
{
	int	value;

	value = num;
	if (power == 0)
		return (1);
	power--;
	while (power > 0)
	{
		value *= num;;
		power--;
	}
	return (value);
}

int	ft_atoi_base(char *str, char *base)
{
	int	base_len;
	int	num;
	int	sign;
	int	i;

	i = 0;
	num = 0;
	sign = 0;
	base_len = check_base(base);
	if (base_len < 1)
		return (0);
	while ((*str >= 7 && *str <= 13) || *str == 32)
		str++;
	while (*str == '-' || *str == '+')
	{
		if (*str == '-')
			sign++;
		str++;
	}
	while (is_in_base(*str, base) > 0)
	{
		i++;
		str++;
	}
	str = str - i;
	i--;
	while (i >= 0)
	{
		num += power(base_len, i) * (is_in_base(*str, base) - 1);
		str++;
		i--;
	}
	if (sign % 2 == 1)
		return (-num);
	return (num);
}
/*
int	main(int ac, char **av)
{
	printf("%d\n", ft_atoi_base(av[1], av[2]));
}
*/
