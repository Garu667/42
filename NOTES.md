# TINY :                                                             

Envie de modifier son appel


# BENCH :                                                             ----------------------> KO !!!

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
[bench] strategy: Adaptive / O(n log n)                             <-------------------------- ERROR
[bench] total_ops: 0
[bench] sa: 0 sb: 0 ss: 0 pa: 0 pb: 0
[bench] ra: 0 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0


# COMPARATIFS CHECKER / CHECKER_LINUX / RESULTS                             ----------------------> OK

➜  PUSH_SWAP git:(main) ✗ ARG="42"; ./push_swap $ARG | ./checker $ARG        
OK
➜  PUSH_SWAP git:(main) ✗ ARG="42"; ./push_swap $ARG | ./checker_linux $ARG 
OK

➜  PUSH_SWAP git:(main) ✗ ARG=""; ./push_swap $ARG | ./checker $ARG       
Error
➜  PUSH_SWAP git:(main) ✗ ARG=""; ./push_swap $ARG | ./checker_linux $ARG 
Error

➜  PUSH_SWAP git:(main) ✗ ARG="1 3 2"; ./push_swap $ARG | ./checker $ARG      
OK
➜  PUSH_SWAP git:(main) ✗ ARG="1 3 2"; ./push_swap $ARG | ./checker_linux $ARG 
OK

➜  PUSH_SWAP git:(main) ✗ ARG="1 2 2"; ./push_swap $ARG | ./checker $ARG      
Error
Error
➜  PUSH_SWAP git:(main) ✗ ARG="1 2 2"; ./push_swap $ARG | ./checker_linux $ARG 
Error
Error

➜  PUSH_SWAP git:(main) ✗ ARG="1 2.5 3"; ./push_swap $ARG | ./checker $ARG      
Error
Error
➜  PUSH_SWAP git:(main) ✗ ARG="1 2.5 3"; ./push_swap $ARG | ./checker_linux $ARG 
Error
Error

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5 -0"; ./push_swap $ARG | ./checker $ARG      
Error
Error
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5 -0"; ./push_swap $ARG | ./checker_linux $ARG 
Error
Error

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --complex $ARG | ./checker_linux $ARG 
OK
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --medium $ARG | ./checker_linux $ARG
OK
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --simple $ARG | ./checker_linux $ARG
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --complex $ARG | ./checker $ARG      
OK
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --medium $ARG | ./checker $ARG      
OK
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --simple $ARG | ./checker $ARG      
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --adaptive $ARG | ./checker_linux $ARG 
OK
➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --adaptive $ARG | ./checker $ARG      
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --bench --adaptive $ARG | ./checker_linux $ARG 
[bench] disorder: 100.00%
[bench] strategy: Adaptive / O(n log n)
[bench] total_ops: 10
[bench] sa: 0 sb: 0 ss: 0 pa: 4 pb: 4
[bench] ra: 2 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --bench --adaptive $ARG | ./checker $ARG      
[bench] disorder: 100.00%
[bench] strategy: Adaptive / O(n log n)
[bench] total_ops: 10
[bench] sa: 0 sb: 0 ss: 0 pa: 4 pb: 4
[bench] ra: 2 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --adaptive --bench $ARG | ./checker_linux $ARG 
[bench] disorder: 100.00%
[bench] strategy: Adaptive / O(n log n)
[bench] total_ops: 10
[bench] sa: 0 sb: 0 ss: 0 pa: 4 pb: 4
[bench] ra: 2 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0
OK

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"; ./push_swap --adaptive --bench $ARG | ./checker $ARG      
[bench] disorder: 100.00%
[bench] strategy: Adaptive / O(n log n)
[bench] total_ops: 10
[bench] sa: 0 sb: 0 ss: 0 pa: 4 pb: 4
[bench] ra: 2 rb: 0 rr: 0 rra: 0 rrb: 0 rrr: 0
OK

➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap $(cat args.txt) | ./checker_linux $(cat args.txt)
OK
➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap $(cat args.txt) | ./checker $(cat args.txt) 
OK

➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap --complex $(cat args.txt) | ./checker_linux $(cat args.txt)
OK
➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap --complex $(cat args.txt) | ./checker $(cat args.txt) 
OK

➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap --complex --simple $(cat args.txt) | ./checker_linux $(cat args.txt)
Error
KO
➜  PUSH_SWAP git:(main) ✗ shuf -i 0-9999 -n 500 > args.txt ; ./push_swap --complex --simple $(cat args.txt) | ./checker $(cat args.txt) 
Error
KO


# COMPARATIFS CHECKER / CHECKER_LINUX / VALGRIND                              ----------------------> OK

# exemple 1 
➜  PUSH_SWAP git:(main) ✗ valgrind ./checker_linux        
==1971256== Memcheck, a memory error detector
==1971256== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1971256== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1971256== Command: ./checker_linux
==1971256== 
==1971256== 
==1971256== HEAP SUMMARY:
==1971256==     in use at exit: 0 bytes in 0 blocks
==1971256==   total heap usage: 1 allocs, 1 frees, 104 bytes allocated
==1971256== 
==1971256== All heap blocks were freed -- no leaks are possible
==1971256== 
==1971256== For lists of detected and suppressed errors, rerun with: -s
==1971256== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./checker      
==1971367== Memcheck, a memory error detector
==1971367== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1971367== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1971367== Command: ./checker
==1971367== 
==1971367== 
==1971367== HEAP SUMMARY:
==1971367==     in use at exit: 0 bytes in 0 blocks
==1971367==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1971367== 
==1971367== All heap blocks were freed -- no leaks are possible
==1971367== 
==1971367== For lists of detected and suppressed errors, rerun with: -s
==1971367== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

# exemple 2
➜  PUSH_SWAP git:(main) ✗ valgrind ./checker_linux 1 2 3
==1971765== Memcheck, a memory error detector
==1971765== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1971765== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1971765== Command: ./checker_linux 1 2 3
==1971765== 
OK
==1971765== 
==1971765== HEAP SUMMARY:
==1971765==     in use at exit: 0 bytes in 0 blocks
==1971765==   total heap usage: 19 allocs, 19 frees, 1,255 bytes allocated
==1971765== 
==1971765== All heap blocks were freed -- no leaks are possible
==1971765== 
==1971765== For lists of detected and suppressed errors, rerun with: -s
==1971765== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./checker 1 2 3      
==1971933== Memcheck, a memory error detector
==1971933== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1971933== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1971933== Command: ./checker 1 2 3
==1971933== 
OK
==1971933== 
==1971933== HEAP SUMMARY:
==1971933==     in use at exit: 0 bytes in 0 blocks
==1971933==   total heap usage: 11 allocs, 11 frees, 128 bytes allocated
==1971933== 
==1971933== All heap blocks were freed -- no leaks are possible
==1971933== 
==1971933== For lists of detected and suppressed errors, rerun with: -s
==1971933== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

# exemple 3 
➜  PUSH_SWAP git:(main) ✗ valgrind ./checker_linux 1 3 2 
==1972770== Memcheck, a memory error detector
==1972770== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1972770== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1972770== Command: ./checker_linux 1 3 2
==1972770== 
KO
==1972770== 
==1972770== HEAP SUMMARY:
==1972770==     in use at exit: 0 bytes in 0 blocks
==1972770==   total heap usage: 19 allocs, 19 frees, 1,255 bytes allocated
==1972770== 
==1972770== All heap blocks were freed -- no leaks are possible
==1972770== 
==1972770== For lists of detected and suppressed errors, rerun with: -s
==1972770== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./checker 1 3 2      
==1972886== Memcheck, a memory error detector
==1972886== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1972886== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1972886== Command: ./checker 1 3 2
==1972886== 
KO
==1972886== 
==1972886== HEAP SUMMARY:
==1972886==     in use at exit: 0 bytes in 0 blocks
==1972886==   total heap usage: 11 allocs, 11 frees, 128 bytes allocated
==1972886== 
==1972886== All heap blocks were freed -- no leaks are possible
==1972886== 
==1972886== For lists of detected and suppressed errors, rerun with: -s
==1972886== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

# exemple 4 
➜  PUSH_SWAP git:(main) ✗ valgrind ./checker_linux 1 3 2 5
==1973197== Memcheck, a memory error detector
==1973197== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1973197== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1973197== Command: ./checker_linux 1 3 2 5
==1973197== 
sa
KO
==1973197== 
==1973197== HEAP SUMMARY:
==1973197==     in use at exit: 0 bytes in 0 blocks
==1973197==   total heap usage: 25 allocs, 25 frees, 2,308 bytes allocated
==1973197== 
==1973197== All heap blocks were freed -- no leaks are possible
==1973197== 
==1973197== For lists of detected and suppressed errors, rerun with: -s
==1973197== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./checker 1 3 2 5      
==1973326== Memcheck, a memory error detector
==1973326== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1973326== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1973326== Command: ./checker 1 3 2 5
==1973326== 
sa
KO
==1973326== 
==1973326== HEAP SUMMARY:
==1973326==     in use at exit: 0 bytes in 0 blocks
==1973326==   total heap usage: 19 allocs, 19 frees, 184 bytes allocated
==1973326== 
==1973326== All heap blocks were freed -- no leaks are possible
==1973326== 
==1973326== For lists of detected and suppressed errors, rerun with: -s
==1973326== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

# exemple 5 
➜  PUSH_SWAP git:(main) ✗ ./checker_linux 1 2 3
valgrind
Error
➜  PUSH_SWAP git:(main) ✗ ./checker_linux 1 3 2
sa
valgrind
Error
➜  PUSH_SWAP git:(main) ✗ ./checker 1 3 2      
valgrind
Error
➜  PUSH_SWAP git:(main) ✗ ./checker_linux 1 3 2
sa
valgrind
Error

# PUSH_SWAP / VALGRIND                              ----------------------> KO

## TEST 1 - 2 - 3 OK

➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap
==1975978== Memcheck, a memory error detector
==1975978== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1975978== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1975978== Command: ./push_swap
==1975978== 
Error
==1975978== 
==1975978== HEAP SUMMARY:
==1975978==     in use at exit: 0 bytes in 0 blocks
==1975978==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1975978== 
==1975978== All heap blocks were freed -- no leaks are possible
==1975978== 
==1975978== For lists of detected and suppressed errors, rerun with: -s
==1975978== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap 42
==1976194== Memcheck, a memory error detector
==1976194== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1976194== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1976194== Command: ./push_swap 42
==1976194== 
==1976194== 
==1976194== HEAP SUMMARY:
==1976194==     in use at exit: 0 bytes in 0 blocks
==1976194==   total heap usage: 4 allocs, 4 frees, 47 bytes allocated
==1976194== 
==1976194== All heap blocks were freed -- no leaks are possible
==1976194== 
==1976194== For lists of detected and suppressed errors, rerun with: -s
==1976194== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap 1 2 3
==1976314== Memcheck, a memory error detector
==1976314== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1976314== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1976314== Command: ./push_swap 1 2 3
==1976314== 
==1976314== 
==1976314== HEAP SUMMARY:
==1976314==     in use at exit: 0 bytes in 0 blocks
==1976314==   total heap usage: 10 allocs, 10 frees, 138 bytes allocated
==1976314== 
==1976314== All heap blocks were freed -- no leaks are possible
==1976314== 
==1976314== For lists of detected and suppressed errors, rerun with: -s
==1976314== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap 1 3 2
==1976422== Memcheck, a memory error detector
==1976422== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1976422== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1976422== Command: ./push_swap 1 3 2
==1976422== 
pb
ra
pb
pb
pa
pa
pa
==1976422== 
==1976422== HEAP SUMMARY:
==1976422==     in use at exit: 0 bytes in 0 blocks
==1976422==   total heap usage: 10 allocs, 10 frees, 138 bytes allocated
==1976422== 
==1976422== All heap blocks were freed -- no leaks are possible
==1976422== 
==1976422== For lists of detected and suppressed errors, rerun with: -s
==1976422== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

➜  PUSH_SWAP git:(main) ✗ ARG="5 0 -5"                                     
➜  PUSH_SWAP git:(main) ✗ valgrind ./push_swap $ARG
==1977887== Memcheck, a memory error detector
==1977887== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1977887== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1977887== Command: ./push_swap 5\ 0\ -5
==1977887== 
pb
ra
pb
pa
pa
ra
pb
pb
pa
pa
==1977887== 
==1977887== HEAP SUMMARY:
==1977887==     in use at exit: 0 bytes in 0 blocks
==1977887==   total heap usage: 8 allocs, 8 frees, 123 bytes allocated
==1977887== 
==1977887== All heap blocks were freed -- no leaks are possible
==1977887== 
==1977887== For lists of detected and suppressed errors, rerun with: -s
==1977887== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

## TEST 5-6 KO ?                                       ----------------------> KO ? (still reachable)

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