/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 13:11:22 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/25 13:13:14 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"
#include <stdio.h>

int	ft_putchar(char c)
{
	return (write(1, &c, 1));
}

int	ft_putstr(char *str)
{
	size_t	i;

	i = -1;
	if (!str)
		return (ft_putstr("(null)"));
	while (str[++i])
		write(1, &str[i], 1);
	return (i);
}

int	ft_putpointer(void *ptr)
{
	unsigned long long int	nbr;
	int						i;

	i = 0;
	if (!ptr)
		return (write(1, "(nil)", 5));
	nbr = (unsigned long long int)ptr;
	i += write(1, "0x", 2);
	i += ft_putnbr_base3(nbr);
	return (i);
}

int	format(const char *str, va_list args)
{
	int	i;

	i = 0;
	if (str[i] == 'c')
		return (ft_putchar(va_arg(args, int)));
	else if (str[i] == 's')
		return (ft_putstr(va_arg(args, char *)));
	else if (str[i] == 'd' || str[i] == 'i')
		return (ft_putnbr_base(va_arg(args, int), "0123456789"));
	else if (str[i] == 'u')
		return (ft_putnbr(va_arg(args, unsigned int)));
	else if (str[i] == 'x')
		return (ft_putnbr_base2(va_arg(args, int), "0123456789abcdef"));
	else if (str[i] == 'X')
		return (ft_putnbr_base2(va_arg(args, int), "0123456789ABCDEF"));
	else if (str[i] == '%')
		return (ft_putchar('%'));
	else if (str[i] == 'p')
		return (ft_putpointer(va_arg(args, void *)));
	else
		return (-1);
}

int	ft_printf(const char *str, ...)
{
	va_list	args;
	int		i;
	int		j;

	i = 0;
	j = 0;
	if (!str)
		return (-1);
	va_start(args, str);
	while (str[j])
	{
		if (str[j] == '%')
		{
			j++;
			i += format((str + j), args);
		}
		else
			i += ft_putchar(str[j]);
		j++;
	}
	va_end(args);
	return (i);
}
/*
int	main(int ac, char **av)
{
	int	ret1;
	int	ret2;
	
	ret1 = ft_printf("%d\n", 0);
	ret2 =    printf("%d\n", 0);
	printf("%d\n", ret1);
	printf("%d\n", ret2);

	ret1 = ft_printf(NULL);
	ret2 =    printf(NULL);
	printf("%d\n", ret1);
	printf("%d\n", ret2);
}
*/
