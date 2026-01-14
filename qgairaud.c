/// 1 ) CHOIX D'ALGO

// Pour ce qui est du choix d'algo, je serai partant pour :

// SIMPLE : Bubble sort adaptation

// En soit, il me semble clairement moins optimisé que le min/max.
// Mais justement, un peu optimisé révèle le besoin de changer d'algo face à
// une liste plus grande.
// Et je trouve qu'il fait une bonne introduction après les modules C01 et C06 de la piscine

// MEDIUM : Bucket sort adaptations with buckets

// Besoin d'une stratégie plus large, les containers me semblent propres, bien définis et concrets.
// Encore une fois, pas sûr que ce soit le plus optimisé des algos mais cela suit une logique de
// difficultés croissante.

// COMPLEX : Radix sort adaptation (en least significant digit)

// Le merge a l'air intéressant mais la division successive puis reconstruction changerait la logique précédente.
// Le quick sort est peut-être le plus optimisé, mais là encore très différent.
// Je n'aime pas trop les deux derniers, heap et binary, qui semblent moins adaptables au projet.


/// 2 ) FONCTIONS / OPERATIONS de base

int     sa(t_stack *a, bool write_switch)
{
    t_node	*first;
	t_node	*second;

	if (!a || !a->top || !a->top->next)
		return (0);
	first = a->top;
	second = first->next;
	first->next = second->next;
	a->top = second;
	second->next = first;
	if (write_switch)
		write(1, "sa\n", 3);
	return (1);
}
int     sb(t_stack *b, bool write_switch)
{
    t_node	*first;
	t_node	*second;

	if (!b || !b->top || !b->top->next)
		return (0);
	first = b->top;
	second = first->next;
	first->next = second->next;
	b->top = second;
	second->next = first;
	if (write_switch)
		write(1, "sb\n", 3);
	return (1);
}
int		ss(t_stack *a, t_stack *b, bool write_switch)
{
    if (!a || !a->top || !a->top->next
        || !b || !b->top || !b->top->next)
        return (0);
    sa(a, false);
    sb(b, false);
	if (write_switch)
		write(1, "ss\n", 3);
    return (1);
}
int		pa(t_stack *a, t_stack *b, bool write_switch)
{
    t_node  *tmp;

    if (!b || !b->top || !a)
        return (0);
    tmp = b->top;
    b->top = b->top->next;
    tmp->next = a->top;
    a->top = tmp;
    a->size++;
    b->size--;
	if (write_switch)
		write(1, "pa\n", 3);
    return (1);
}
int		pb(t_stack *b, t_stack *a, bool write_switch)
{
    t_node  *tmp;

    if (!a || !a->top || !b)
        return (0);
    tmp = a->top;
    a->top = a->top->next;
    tmp->next = b->top;
    b->top = tmp;
    b->size++;
    a->size--;
	if (write_switch)
		write(1, "pb\n", 3);
    return (1);
}
