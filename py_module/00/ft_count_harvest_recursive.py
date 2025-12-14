def ft_count_harvest_recursive(day = None, i = 1):
    if (day == None):
        day = int(input("Days until harvest: "))
    if (i > day):
        print("Harvest time!")
        return
    print("Day", i)
    ft_count_harvest_recursive(day, i + 1)
