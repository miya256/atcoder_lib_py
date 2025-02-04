def groups(a,group=[]):
    if not a:
        print(group)
        return
    first,rest = a[0],a[1:]
    for i in range(len(group)):
        new_group = [list(j) for j in group]
        new_group[i].append(first)
        groups(rest,new_group)
    groups(rest,group+[[first]])

a = [1,2,3]
groups(a)