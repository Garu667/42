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
	if (!str || str[0] == 0)
		return (0);
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
		return (NULL);
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
		bytes_read = read(0, (str + size), 1); // Dois lire BUFFER_SIZE aulieu de 1
	}
	return (str);
}

char	*get_next_line(int fd)
{
	char	*line;

	line = malloc(sizeof(char));
	if (!line)
		return (NULL);
	if (fd < 0 || BUFFER_SIZE <= 0)
		return (free(line), NULL);
	line = ft_get_line(fd, line);
	if (!line)
		return (free(line), NULL);
	return (line);
}

int	main(int ac, char **av)
{
	int	i;
	int	fd;
	char	*line;

	i = 0;
	fd = 0;
	line = NULL;
	if (ac == 2)
	{
		fd = open(av[1], O_RDONLY);
		if (fd == -1)
			return (-1);
	}
	line = get_next_line(fd);
	while (line && i++ != 4)
	{
		printf("%s", line);
		line = get_next_line(fd);
	}
	free(line);
}
