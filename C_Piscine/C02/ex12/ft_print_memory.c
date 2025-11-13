#include <stdlib.h>
#include <unistd.h>

void	ft_putnbr(int nb)
{
	unsigned int	nbr;

	nbr = nb;
	if (nb < 0)
	{
		write(1, "-", 1);
		nbr = nb * -1;
	}
	if (nbr >= 10)
		ft_putnbr(nbr / 10);
	nbr = (nbr % 10) + 48;
	write(1, (char *)&nbr, 1);
}

void	ft_putnbr_base(int nb, int i)
{
	unsigned int	nbr;
	char			*base;

	base = "0123456789abcdef";
	if (nb < 0)
	{
		write(1, "-", 1);
		nbr = nb * -1;
	}
	else
		nbr = nb;
	if (nbr >= 16)
		ft_putnbr_base(nbr / 16, ++i);
	if (i == 1)
		write(1, "0", 1);
	write(1, (char *)&base[nbr % 16], 1);
}

void	display_new_line( unsigned int i, unsigned int line_count)
{
	unsigned int k;

	if (i > 0)
		write(1, "\n", 1);
	k = (line_count == 0 ? 1 : line_count);
	while ((k *= 10) < 10000000)
		write(1, "0", 1);
	ft_putnbr(line_count * 10);
	if (line_count == 0)
		write(1, "0", 1);
	write(1, ": ", 2);
}

void	display_hexa(char *str)
{
	int	count;

	count = 0;
	while (count < 16)
	{
		ft_putnbr_base(str[count], 1);
		if (count % 2 == 1)
			write(1, " ", 1);
		count++;
	}
	write(1, " ", 1);
}

void	*ft_print_memory(void *addr, unsigned int size)
{
	unsigned int	i; // Traverse la str
	unsigned int	j; // Compte la taille des lignes
	unsigned int	k; // Compte les lignes
	char			*str;

	str = (char *)addr;
	i = 0;
	j = 1;
	k = 0;
	while (i < size)
	{
		if (i == 0)
		{
			display_new_line(i, k);
			display_hexa(str + i);
		}
		if (str[i] >= 32 && str[i] != 127)
			write(1, &str[i], 1);
		else
			write(1, ".", 1);
		if (j == 16)
		{
			k++;
			display_new_line(i, k);
			display_hexa(str + i + 1);
			j = 0;
		}
		i++;
		j++;
	}
	write(1, "\n", 1);
	return (addr);
}

int	ft_strlen(char *str)
{
	int	count;

	count = 0;
	while (str[count])
		count++;
	return (count);
}
/*
int	main(int argc, char *argv[])
{
	ft_print_memory((char*)argv[1], (unsigned int)ft_strlen(argv[1]));
	return (0);
}
*/
