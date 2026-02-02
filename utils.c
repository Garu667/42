/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:39 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:39 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static bool	check_int_min(int sign, long nb)
{
	if ((sign == 1 && nb > INT_MAX) || (sign == -1 && nb > ((long)INT_MAX + 1)))
		return (0);
	return (1);
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
		if (check_int_min(sign, nb) == 0)
			return (0);
		nb = nb * 10 + (*str++ - 48);
		i++;
	}
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (i == 0 || check_int_min(sign, nb) == 0 || *str != 0)
		return (0);
	*nbr = (int)(nb * sign);
	return (i);
}

static void	free_stack(t_stack *stack)
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

static void	free_split(char **split, int indx)
{
	while (split[indx])
	{
		free(split[indx]);
		indx++;
	}
	free(split);
}

int	free_all(t_stack *stack, char **split, int flag)
{
	if (flag == 1)
	{
		free_split(split, 0);
		free_stack(stack);
	}
	else if (flag == 2)
		free_split(split, 0);
	else if (flag == 3)
		free_stack(stack);
	return (1);
}
