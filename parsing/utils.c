/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:54 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/24 15:25:51 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

void	ft_safe_write(int fd, char *str, int len)
{
	if (write(fd, str, len) == -1)
	{
		write(2, "Error\n", 6);
		exit(EXIT_FAILURE);
	}
}

bool	is_sorted(t_stack *a)
{
	t_node	*current;
	int		i;

	if (!a || !a->head || a->size <= 1)
		return (true);
	current = a->head;
	i = 0;
	while (i < (a->size - 1))
	{
		if (current->value > current->next->value)
			return (false);
		current = current->next;
		i++;
	}
	return (true);
}

int	ft_putstr_fd(char *s, int fd)
{
	size_t	i;

	i = -1;
	while (s[++i])
		write(fd, &s[i], 1);
	return (i);
}

void	ft_putnbr_fd(int n, int fd)
{
	char	c;

	if (n == -2147483648)
	{
		ft_safe_write(fd, "-2147483648", 11);
		return ;
	}
	if (n < 0)
	{
		ft_safe_write(fd, "-", 1);
		n = -n;
	}
	if (n < 10)
	{
		c = (n + 48);
		ft_safe_write(fd, &c, 1);
	}
	if (n > 9)
	{
		ft_putnbr_fd((n / 10), fd);
		c = ((n % 10) + 48);
		ft_safe_write(fd, &c, 1);
	}
}

int	ft_atoi(const char *str, int *nbr)
{
	long	nb;
	int		sign;
	int		i;

	i = 0;
	nb = 0;
	sign = 1;
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (*str == '-' || *str == '+')
		if (*str++ == '-')
			sign *= -1;
	while (*str >= '0' && *str <= '9')
	{
		nb = nb * 10 + (*str++ - 48);
		i++;
	}
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (i == 0 || (sign == 1 && nb > INT_MAX)
		|| (sign == -1 && nb > ((long)INT_MAX + 1)) || *str != 0)
		exit(write(2, "Error\n", 6));
	*nbr = (int)(nb * sign);
	return (i);
}
