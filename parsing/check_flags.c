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

static void	ft_check2(int *flag, int flag_bits)
{
	if (flag_bits & FLAG_BENCH && !((*flag) & (FLAG_BENCH)))
		(*flag) |= flag_bits;
	else if (flag_bits > 1 && !((*flag)
			& (FLAG_SIMPLE | FLAG_MEDIUM | FLAG_COMPLEX | FLAG_ADAPTIVE)))
		(*flag) |= flag_bits;
	else
		exit(write(2, "Error\n", 6));
}

static void	ft_check(char *str, int *flag)
{
	if (ft_strncmp(str, "--bench\0", 8) == 0)
		ft_check2(flag, FLAG_BENCH);
	else if (ft_strncmp(str, "--simple\0", 9) == 0)
		ft_check2(flag, FLAG_SIMPLE);
	else if (ft_strncmp(str, "--medium\0", 9) == 0)
		ft_check2(flag, FLAG_MEDIUM);
	else if (ft_strncmp(str, "--complex\0", 11) == 0)
		ft_check2(flag, FLAG_COMPLEX);
	else if (ft_strncmp(str, "--adaptive\0", 11) == 0)
		ft_check2(flag, FLAG_ADAPTIVE);
	else
		exit(write(2, "Error\n", 6));
}

int	ft_check_flag(char **av, int ac)
{
	int	flag;
	int	i;

	i = 1;
	flag = 0;
	while (i < ac)
	{
		if (av[i][0] == '-' && av[i][1] == '-')
			ft_check(av[i], &flag);
		i++;
	}
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

int	free_all(t_stack *stack, char **split)
{
	free_split(split, 0, 3);
	free_stack(stack);
	return (1);
}
