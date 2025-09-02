#include "header.h"

char	*ft_realloc(char *str, int size, int new_capacity)
{
	char	*new_str;
	int		i;

	new_str = malloc(new_capacity);
	if (!new_str)
		return (free(str), NULL);
	i = -1;
	while (++i < size)
		new_str[i] = str[i];
	free(str);
	return (new_str);
}

int	ft_check_line(char *str)
{
	int	i;

	i = -1;
	while (str[++i])
		if (str[i] == '\n')
			return (1);
	return (0);
}

char	*ft_get_line(int fd, char *str)
{
	long	bytes_read;
	int		size;
	int		capacity;

	size = 0;
	capacity = BUFFER_SIZE;
	bytes_read = read(0, (str + size), 1);
	if (!str || bytes_read == 0)
		return (free(str), NULL);
	while (ft_check_line(str) == 0 && bytes_read > 0)
	{
		size += bytes_read;
		if (size + BUFFER_SIZE > capacity)
		{
			capacity += BUFFER_SIZE;
			str = ft_realloc(str, size, capacity + 1);
			if (!str)
				return (NULL);
		}
		str[size] = '\0';
		bytes_read = read(0, (str + size), 1);
	}
	return (str);
}

char	*get_next_line(int fd)
{
	char	*line;

	line = malloc(1);
	if (fd < 0 || BUFFER_SIZE <= 0 || !line)
		return (free(line), NULL);
	if (line == NULL)
		return (NULL);
}

int	main(int ac, char **av)
{
	int	fd;
	char	*line;

	fd = 0;
	line = NULL;
	if (ac == 2)
	{
		fd = open(av[1], O_RDONLY);
		if (fd == -1)
			return (-1);
	}
	line = ft_get_line(fd);
	while (line)
	{
		printf("%s", line);
		line = ft_get_line(fd);
	}
	free(line);
}
