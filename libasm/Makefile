TEST_SRC	:= main.c

SRCS		:= src/ft_strlen.s	\
			   src/ft_strcpy.s	\
			   src/ft_strcmp.s	\
			   src/ft_strdup.s
OBJS		:= $(SRCS:.s=.o)

#BONUS		:= ft_lstnew_bonus.c
#BONUS_OBJS	:= $(BONUS:.c=.o)

CC			:= cc
AS			:= nasm
RM			:= rm -f
CFLAGS		:= -Wall -Werror -Wextra
ASFLAGS		:= -f elf64 -w+all -w+error
#INC		:= include/libasm.inc
NAME		:= libasm.a
TEST_NAME	:= main

$(NAME):	$(OBJS) # $(SRC_INCLUDES)
			ar rcs $(NAME) $(OBJS)

%.o:		%.asm #$(INC)
			$(AS) $(ASFLAGS) $< -o $@

all:		$(NAME)

clean:
			$(RM) $(OBJS)

fclean:		clean
			$(RM) $(NAME) $(TEST_NAME)

re:			fclean all

test:		$(NAME) $(TEST_SRC)
			$(CC) $(CFLAGS) $(TEST_SRC) -L. -lasm -o $(TEST_NAME)

#bonus:		.bonus

#.bonus:		$(OBJS) $(BONUS_OBJS)
#			ar rcs $(NAME) $(OBJS) $(BONUS_OBJS)
#			touch .bonus

.PHONY:		all clean fclean re test #bonus
