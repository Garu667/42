# LEAKS si doublons de int ou erreurs d'arguments, dans chaque programme  :

==61195== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
➜  BINOME git:(main) ✗ valgrind ./push_swap 1 2 3 3
==61301== Memcheck, a memory error detector
==61301== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==61301== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==61301== Command: ./push_swap 1 2 3 3
==61301== 
Error
==61301== 
==61301== HEAP SUMMARY:
==61301==     in use at exit: 72 bytes in 3 blocks
==61301==   total heap usage: 11 allocs, 8 frees, 144 bytes allocated
==61301== 
==61301== LEAK SUMMARY:
==61301==    definitely lost: 24 bytes in 1 blocks
==61301==    indirectly lost: 48 bytes in 2 blocks
==61301==      possibly lost: 0 bytes in 0 blocks
==61301==    still reachable: 0 bytes in 0 blocks
==61301==         suppressed: 0 bytes in 0 blocks
==61301== Rerun with --leak-check=full to see details of leaked memory
==61301== 
==61301== For lists of detected and suppressed errors, rerun with: -s
==61301== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)






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