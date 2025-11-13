#include <stdio.h>
#include <unistd.h>

#define ISPRINT(c) (c >= 32 && c <= 126)

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

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

void	ft_putnbr_base(int nbr, char *base)
{
	int	base_len;
	long int	n;

	base_len = check_base(base);
	n = nbr;
	if (base_len <= 1)
		return ;
	if (n < 0)
	{
		ft_putchar('-');
		n = -n;
	}
	if (n < base_len)
		ft_putchar(base[n]);
	if (n >= base_len)
	{
		ft_putnbr_base(n / base_len, base);
		ft_putchar(base[(n % base_len)]);
	}
}

void	ft_putstr_non_printable(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (!ISPRINT(str[i]))
		{
			ft_putchar('\\');
			if (str[i] <= '\xf')
				ft_putchar('0');
			ft_putnbr_base(str[i++], "0123456789abcdef");
		}
		else
		{
			ft_putchar(str[i]);
			i++;
		}
	}
}

/*
int	main(void)
{
	ft_putstr_non_printable("Coucou\n sava");
	char	c = '\n';
	printf("%d\n", c);
}
*/
