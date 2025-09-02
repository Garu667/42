#ifndef HEADER_H
# define HEADER_H
# define BUFFER_SIZE 32

# include <stdlib.h>
# include <unistd.h>
# include <fcntl.h>
# include <stdio.h>
# include <stddef.h>

typedef struct s_fd_data
{
	char	*rest;
	int		fd;
	struct s_fd_data	*next;
}	t_fd_data;

#endif
