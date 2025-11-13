/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: saidriss <saidriss@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/09/21 20:04:17 by saidriss          #+#    #+#             */
/*   Updated: 2024/09/21 22:44:09 by saidriss         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <unistd.h>

int	already_here(int grid[4][4], int row, int col, int num);

int	check_col(int grid[4][4], int *constraints, int x);

int	check_row(int grid[4][4], int *constraints, int y);

int	check_all(int grid[4][4], int *constraints);

int	solve_puzzle(int grid[4][4], int *constraints, int row, int col);

void	ft_putstr(char *str)
{
	while (*str)
		write(1, str++, 1);
}

void	print_grid(int grid[4][4])
{
	int		i;
	int		j;
	char	c;

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			c = grid[i][j] + '0';
			write(1, &c, 1);
			if (j < 3)
				write(1, " ", 1);
			j++;
		}
		write(1, "\n", 1);
		i++;
	}
}

int	valid_input(char *input, int *constraints)
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (i < 16)
	{
		while (input[j] == ' ')
			j++;
		if (input[j] >= '1' && input[j] <= '4')
		{
			constraints[i] = input[j] - '0';
			i++;
			j++;
		}
		else
			return (0);
	}
	return (1);
}

int	**init_grid(int grid[4][4])
{
	int	i;
	int	j;

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			grid[i][j] = 0;
			j++;
		}
		i++;
	}
	return (0);
}

int	main(int argc, char **argv)
{
	int	grid[4][4];
	int	constraints[16];

	if (argc != 2 || !valid_input(argv[1], constraints))
	{
		ft_putstr("Error\n");
		return (1);
	}
	init_grid(grid);
	if (!solve_puzzle(grid, constraints, 0, 0))
		ft_putstr("Error\n");
	else
		print_grid(grid);
	return (0);
}
