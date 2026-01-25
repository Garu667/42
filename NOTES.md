# BENCH :                                                             corrigé mais salement ?

➜  PUSH_SWAP git:(main) ✗ ./push_swap --bench 1 2 3

[bench] disorder: 0.00%
[bench] strategy: [bench] total_ops: 0                              <------------------------- ERROR
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0

➜  PUSH_SWAP git:(main) ✗ ./push_swap --bench --simple 1 2 3

[bench] disorder: 0.00%
[bench] strategy: Simple / O(n²)
[bench] total_ops: 0
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0

➜  PUSH_SWAP git:(main) ✗ ./push_swap --bench --medium 1 2 3 

[bench] disorder: 0.00%
[bench] strategy: Medium / O(n√n[bench] total_ops: 0                <-------------------------- ERROR      
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0

➜  PUSH_SWAP git:(main) ✗ ./push_swap --bench --complex 1 2 3

[bench] disorder: 0.00%
[bench] strategy: Complex / O(n log n)
[bench] total_ops: 0
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0

➜  PUSH_SWAP git:(main) ✗ ./push_swap --bench --adaptive 1 2 3

[bench] disorder: 0.00%
[bench] strategy: Adaptive / O(n log n)                            <-------------------------- ERROR
[bench] total_ops: 0
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0


# PUSH_SWAP / VALGRIND      (remplacer les exit par free_stack dans parsing + parsing_multiple + ft_atoi ?)


➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap 1 3 2 3
==1977150== Memcheck, a memory error detector
==1977150== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1977150== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1977150== Command: ./push_swap 1 3 2 3
==1977150== 
Error
==1977150== 
==1977150== HEAP SUMMARY:
==1977150==     in use at exit: 90 bytes in 5 blocks
==1977150==   total heap usage: 11 allocs, 6 frees, 144 bytes allocated
==1977150== 
==1977150== LEAK SUMMARY:
==1977150==    definitely lost: 0 bytes in 0 blocks
==1977150==    indirectly lost: 0 bytes in 0 blocks
==1977150==      possibly lost: 0 bytes in 0 blocks
==1977150==    still reachable: 90 bytes in 5 blocks
==1977150==         suppressed: 0 bytes in 0 blocks
==1977150== Rerun with --leak-check=full to see details of leaked memory
==1977150== 
==1977150== For lists of detected and suppressed errors, rerun with: -s
==1977150== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 0"              
➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap $ARG
==1978773== Memcheck, a memory error detector
==1978773== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1978773== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1978773== Command: ./push_swap 5\ 0\ 0
==1978773== 
Error
==1978773== 
==1978773== HEAP SUMMARY:
==1978773==     in use at exit: 86 bytes in 6 blocks
==1978773==   total heap usage: 6 allocs, 0 frees, 86 bytes allocated
==1978773== 
==1978773== LEAK SUMMARY:
==1978773==    definitely lost: 0 bytes in 0 blocks
==1978773==    indirectly lost: 0 bytes in 0 blocks
==1978773==      possibly lost: 0 bytes in 0 blocks
==1978773==    still reachable: 86 bytes in 6 blocks
==1978773==         suppressed: 0 bytes in 0 blocks
==1978773== Rerun with --leak-check=full to see details of leaked memory
==1978773== 
==1978773== For lists of detected and suppressed errors, rerun with: -s
==1978773== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)


# RECODING                                                          (à réfléchir)

Apparemment, il s'agit de
- creer un flag
- qui stoppe l'affichage des operations
- sans empecher le tri
- et affiche le nombre total des operations