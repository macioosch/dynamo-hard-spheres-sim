for i in {1..10}; do for f in jobs/convergence-d.*.sh; do qsub $f; done; echo $i; done
