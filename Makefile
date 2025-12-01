# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/12 18:08:48 by ramaroud          #+#    #+#              #
#    Updated: 2025/11/25 13:11:07 by ramaroud         ###   ########lyon.fr    #
#                                                                              #
# **************************************************************************** #

SRCS	= ft_printf.c	\
		  utils.c
OBJ	= $(SRCS:.c=.o)
ALL_D	= $(SRCS:.c=.d)


CFLAGS		= -Wall -Wextra -Werror -MMD -MP
RM		= rm -f
AR		= ar rcs
INC		= ft_printf.h

NAME		= libftprintf.a

all:		$(NAME)

$(NAME):	$(OBJ) $(INC)
			$(AR) $(NAME) $(OBJ)

clean:
			$(RM) $(OBJ) $(ALL_D)

fclean:		clean
			$(RM) $(NAME)

re:	fclean all

-include $(ALL_D)

.PHONY: all clean fclean re
