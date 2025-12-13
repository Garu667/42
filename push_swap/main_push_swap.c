/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 19:42:14 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/12 19:42:17 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	main(int ac, char **av)
{
	t_stack	a;
	int		i;

	i = 1;
	if (ac < 1)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av, i);
	push_swap(&a, ac, ft_compute_disorder(a));
	free(a.tab);
}
