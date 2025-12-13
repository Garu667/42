/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ramaroud.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:53:19 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/13 01:53:21 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	ft_check2(int *flag, int *count, int flag_bits)
{
	if (flag_bits == FLAG_BENCH)
	{
		(*flag) |= flag_bits;
		(*count)++;
		return ;
	}
	if ((*flag) & (FLAG_SIMPLE | FLAG_MEDIUM | FLAG_COMPLEXE | FLAG_ADAPTIVE))
		exit(write(2, "Error\n", 6));
	(*flag) |= flag_bits;
	(*count)++;
}

static int	ft_check(char *str, int *flag)
{
	int	count;

	count = 0;
	if (ft_strncmp(str, "--bench", 7) == 0)
		ft_check2(flag, &count, FLAG_BENCH);
	else if (ft_strncmp(str, "--simple", 8) == 0)
		ft_check2(flag, &count, FLAG_SIMPLE);
	else if (ft_strncmp(str, "--medium", 8) == 0)
		ft_check2(flag, &count, FLAG_MEDIUM);
	else if (ft_strncmp(str, "--complexe", 10) == 0)
		ft_check2(flag, &count, FLAG_COMPLEXE);
	else if (ft_strncmp(str, "--adaptive", 10) == 0)
		ft_check2(flag, &count, FLAG_ADAPTIVE);
	else
		exit(write(2, "Error\n", 6));
	return (count);
}

int	ft_check_flag(char **av, int *i)
{
	int	flag;
	int	ret;
	int	j;

	if (av[*i][0] != '-' && av[*i][1] != '-')
		return (0);
	flag = 0;
	ret = 0;
	j = 0;
	while (av[*i + j] && j < 2)
	{
		if (av[*i + j][0] == '-' && av[*i + j][1] == '-')
			ret += ft_check(av[(*i) + j], &flag);
		else
			break ;
		j++;
	}
	(*i) += ret;
	return (flag);
}
