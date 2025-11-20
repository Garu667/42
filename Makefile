# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/12 18:08:48 by ramaroud          #+#    #+#              #
#    Updated: 2025/11/20 13:32:23 by ramaroud         ###   ########lyon.fr    #
#                                                                              #
# **************************************************************************** #

SRCS	= ft_isdigit.c		\
	  ft_isalnum.c		\
	  ft_isascii.c		\
	  ft_isprint.c		\
	  ft_strlen.c		\
	  ft_memset.c		\
	  ft_isalpha.c		\
	  ft_bzero.c		\
	  ft_memcpy.c		\
	  ft_memmove.c		\
	  ft_strlcpy.c		\
	  ft_strlcat.c		\
	  ft_toupper.c		\
	  ft_tolower.c		\
	  ft_strchr.c		\
	  ft_strrchr.c		\
	  ft_strncmp.c		\
	  ft_memchr.c		\
	  ft_memcmp.c		\
	  ft_strnstr.c		\
	  ft_atoi.c		\
	  ft_calloc.c		\
	  ft_strdup.c		\
	  ft_substr.c		\
	  ft_strjoin.c		\
	  ft_strtrim.c		\
	  ft_split.c		\
	  ft_itoa.c		\
	  ft_strmapi.c		\
	  ft_striteri.c		\
	  ft_putchar_fd.c	\
	  ft_putstr_fd.c	\
	  ft_putendl_fd.c	\
	  ft_putnbr_fd.c
OBJS	= $(SRCS:.c=.o)

BONUS = ft_lstnew_bonus.c		\
	ft_lstadd_front_bonus.c		\
	ft_lstsize_bonus.c 		\
	ft_lstlast_bonus.c		\
	ft_lstadd_back_bonus.c		\
	ft_lstdelone_bonus.c		\
	ft_lstclear_bonus.c		\
	ft_lstiter_bonus.c		\
	ft_lstmap_bonus.c
BONUS_OBJS = $(BONUS:.c=.o)

CC		= cc
RM		= rm -f
CFLAGS		= -Wall -Wextra -Werror
SRC_INCLUDES	= libft.h

NAME	= libft.a

all:		$(NAME)

$(NAME):	$(OBJS) $(SRC_INCLUDES)
			ar rcs $(NAME) $(OBJS)

clean:
			$(RM) $(OBJS) $(BONUS_OBJS)

fclean:		clean
			$(RM) $(NAME)
			$(RM) .bonus

re:		fclean all

bonus:		.bonus

.bonus:		$(OBJS) $(BONUS_OBJS)
			ar rcs $(NAME) $(OBJS) $(BONUS_OBJS)
			touch .bonus

%.o:		%.c libft.h
			$(CC) $(CFLAGS) -c $< -o $@

.PHONY:		all clean fclean re bonus
