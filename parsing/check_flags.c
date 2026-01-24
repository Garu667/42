/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_flags.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:13 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/24 15:38:17 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

static void	ft_check2(int *flag, int *count, int flag_bits)
{
	if (flag_bits == FLAG_BENCH)
	{
		(*flag) |= flag_bits;
		(*count)++;
		return ;
	}
	if ((*flag) & (FLAG_SIMPLE | FLAG_MEDIUM | FLAG_COMPLEX | FLAG_ADAPTIVE))
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
	else if (ft_strncmp(str, "--complex", 10) == 0)
		ft_check2(flag, &count, FLAG_COMPLEX);
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

void	free_stack(t_stack *stack)
{
	t_node	*current;
	t_node	*next;
	int		i;

	if (!stack || !stack->head)
		return ;
	i = 0;
	current = stack->head;
	while (i < stack->size)
	{
		next = current->next;
		free(current);
		current = next;
		i++;
	}
	stack->head = NULL;
	stack->size = 0;
}
