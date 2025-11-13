#include <stdio.h>
#include <stdlib.h>

int	ft_add(int a, int b)
{
	return (a + b);
}

int	ft_sub(int a, int b)
{
	return (a - b);
}

int	ft_mul(int a, int b)
{
	return (a * b);
}

int	ft_div(int a, int b)
{
	return (a / b);
}

int	ft_mod(int a, int b)
{
	return (a % b);
}

void	ft_doop(int(*f)(int, int), int a, int b)
{
	printf("%d\n", f(a, b));
}

int	main(int ac, char **av)
{
	int	a;
	int	b;

	if (ac != 4)
		return (1);
	a = atoi(av[1]);
	b = atoi(av[3]);
	if (av[2][0] == '/' && b == 0)
	{
		printf("Stop : division by zero\n");
		return (1);
	}
	if (av[2][0] == '%' && b == 0)
	{
		printf("Stop : modulo by zero\n");
		return (1);
	}
	if (av[2][0] == '+')
		ft_doop(&ft_add, a, b);
	if (av[2][0] == '-')
		ft_doop(&ft_sub, a, b);
	if (av[2][0] == '*')
		ft_doop(&ft_mul, a, b);
	if (av[2][0] == '/')
		ft_doop(&ft_div, a, b);
	if (av[2][0] == '%')
		ft_doop(&ft_mod, a, b);
	else
		printf("0\n");
}
