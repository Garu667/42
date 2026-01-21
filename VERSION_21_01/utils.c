/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:50 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 18:59:49 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static char	*ft_substr(char *s, unsigned int start, size_t len)
{
	size_t	i;
	char	*substr;

	i = 0;
	if (len > ft_strlen(s + start))
		len = ft_strlen(s + start);
	substr = malloc(sizeof(char) * (len + 1));
	if (!substr)
		return (NULL);
	while (i < len)
	{
		substr[i] = s[start + i];
		i++;
	}
	substr[i] = 0;
	return (substr);
}

static char	*ft_strchr(char *s, int c)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)s + i);
		i++;
	}
	if (s[i] == (char)c)
		return ((char *)s + i);
	return (NULL);
}

char	*ft_strtrim(char *s1, char *set)
{
	size_t	j;

	if (!s1 || !set)
		return (0);
	while (*s1 && ft_strchr(set, *s1))
		s1++;
	j = ft_strlen(s1);
	while (j != 0 && ft_strchr(set, s1[j]))
		j--;
	return (ft_substr(s1, 0, j + 1));
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
