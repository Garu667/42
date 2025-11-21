/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/15 13:37:24 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/17 18:38:41 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_intlen(long nbr)
{
	long	nb;
	int		i;

	i = 0;
	nb = nbr;
	if (nb < 0)
	{
		nb = -nb;
		i++;
	}
	if (nb == 0)
		i++;
	while (nb != 0)
	{
		nb /= 10;
		i++;
	}
	return (i);
}

char	*ft_itoa(int n)
{
	long	nbr;
	int		i;
	int		len;
	char	*num;

	i = 0;
	nbr = n;
	len = ft_intlen(nbr);
	num = malloc(sizeof(char) * (len + 1));
	if (!num)
		return (NULL);
	num[0] = '0';
	if (nbr < 0)
		nbr = -nbr;
	i = len - 1;
	while (nbr != 0)
	{
		num[i--] = (nbr % 10) + 48;
		nbr /= 10;
	}
	if (n < 0)
		num[0] = '-';
	num[len] = 0;
	return (num);
}
