/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 09:56:19 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/01 09:56:26 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(unsigned int n)
{
	int	i;

	i = 0;
	if (n >= 0 && n < 10)
		i += ft_putchar((n + 48));
	else
	{
		i += ft_putnbr(n / 10);
		i += ft_putnbr(n % 10);
	}
	return (i);
}

int	ft_putnbr_base(int nbr, char *base)
{
	int	base_len;
	int	i;

	i = 0;
	base_len = 0;
	while (base[base_len])
		base_len++;
	if (nbr == -2147483648)
	{
		write(1, "-2147483648", 11);
		return (11);
	}
	if (nbr < 0)
	{
		i += ft_putchar('-');
		nbr = -nbr;
	}
	if (nbr >= base_len)
		i += ft_putnbr_base(nbr / base_len, base);
	i += ft_putchar(base[(nbr % base_len)]);
	return (i);
}

int	ft_putnbr_base2(unsigned int nbr, char *base)
{
	unsigned int	base_len;
	int				i;

	i = 0;
	base_len = 0;
	while (base[base_len])
		base_len++;
	if (nbr >= base_len)
		i += ft_putnbr_base2(nbr / base_len, base);
	i += ft_putchar(base[(nbr % base_len)]);
	return (i);
}

int	ft_putnbr_base3(unsigned long long int nbr)
{
	char	*base;
	int		i;

	i = 0;
	base = "0123456789abcdef";
	if (nbr >= 16)
		i += ft_putnbr_base3(nbr / 16);
	i += ft_putchar(base[(nbr % 16)]);
	return (i);
}
