int	sa(t_stack *a, bool write_switch)
{
	t_node	*first;
	t_node	*second;

	if (!a || !a->head || !a->head->next)
		return (0);
	first = a->head;
	second = first->next;
	first->next = second->next;
	a->head = second;
	second->next = first;
	if (write_switch)
		write(1, "sa\n", 3);
	return (1);
}

int	sb(t_stack *b, bool write_switch)
{
	t_node	*first;
	t_node	*second;

	if (!b || !b->head || !b->head->next)
		return (0);
	first = b->head;
	second = first->next;
	first->next = second->next;
	b->head = second;
	second->next = first;
	if (write_switch)
		write(1, "sb\n", 3);
	return (1);
}

int	ss(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	sa(a, false);
	sb(b, false);
	if (write_switch)
		write(1, "ss\n", 3);
	return (1);
}

int	pa(t_stack *a, t_stack *b, bool write_switch)
{
	t_node	*tmp;

	if (!b || !b->head || !a)
		return (0);
	tmp = b->head;
	b->head = b->head->next;
	tmp->next = a->head;
	a->head = tmp;
	a->size++;
	b->size--;
	if (write_switch)
		write(1, "pa\n", 3);
	return (1);
}

int	pb(t_stack *b, t_stack *a, bool write_switch)
{
	t_node	*tmp;

	if (!a || !a->head || !b)
		return (0);
	tmp = a->head;
	a->head = a->head->next;
	tmp->next = b->head;
	b->head = tmp;
	b->size++;
	a->size--;
	if (write_switch)
		write(1, "pb\n", 3);
	return (1);
}

int	ra(t_stack *a, bool write_switch)
{
	t_node	*first;
	t_node	*last;

	if (!a || !a->head || !a->head->next)
		return (0);
	first = a->head;
	a->head = a->head->next;
	first->next = NULL;
	last = a->head;
	while (last->next)
		last = last->next;
	last->next = first;
	if (write_switch)
		write(1, "ra\n", 3);
	return (1);
}

int	rb(t_stack *b, bool write_switch)
{
	t_node	*first;
	t_node	*last;

	if (!b || !b->head || !b->head->next)
		return (0);
	first = b->head;
	b->head = b->head->next;
	first->next = NULL;
	last = b->head;
	while (last->next)
		last = last->next;
	last->next = first;
	if (write_switch)
		write(1, "rb\n", 3);
	return (1);
}

int	rr(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	ra(a, false);
	rb(b, false);
	if (write_switch)
		write(1, "rr\n", 3);
	return (1);
}

int	rra(t_stack *a, bool write_switch)
{
	t_node	*pre_last;
	t_node	*last;

	if (!a || !a->head || !a->head->next)
		return (0);
	pre_last = a->head;
	while (pre_last->next->next)
		pre_last = pre_last->next;
	last = pre_last->next;
	pre_last->next = NULL;
	last->next = a->head;
	a->head = last;
	if (write_switch)
		write(1, "rra\n", 4);
	return (1);
}

int	rrb(t_stack *b, bool write_switch)
{
	t_node	*pre_last;
	t_node	*last;

	if (!b || !b->head || !b->head->next)
		return (0);
	pre_last = b->head;
	while (pre_last->next->next)
		pre_last = pre_last->next;
	last = pre_last->next;
	pre_last->next = NULL;
	last->next = b->head;
	b->head = last;
	if (write_switch)
		write(1, "rrb\n", 4);
	return (1);
}

int	rrr(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	rra(a, false);
	rrb(b, false);
	if (write_switch)
		write(1, "rrr\n", 4);
	return (1);
}
