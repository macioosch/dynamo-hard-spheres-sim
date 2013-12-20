#!/usr/bin/gnuplot
set terminal pdf enhanced mono dashed font "CMU Serif,13"

system("[ -f fit.log ] && rm fit.log")

set datafile separator "\t"
file = "csv/uniform.csv"

d1_file = "csv/dzmd-dzeta-uniform-cropped.csv"
d1_first = "csv/dzmd-dzeta-uniform-first.csv"
d1_last = "csv/dzmd-dzeta-uniform-last.csv"

a1 = -1.64
b1 = 18.7
y1(x) = b1*x + a1
fit y1(x) file u 1:6 via a1,b1

a2 = 2.85
b2 = -13.3
c2 = 56.9
y2(x) = c2*x**2 + b2*x + a2
fit y2(x) file u 1:6 via a2,b2,c2

a3 = -2.85
b3 = 13.3
c3 = -56.9
d3 = 100.0
y3(x) = d3*x**3 + c3*x**2 + b3*x + a3
fit y3(x) file u 1:6 via a3,b3,c3,d3

unset key
set format x "%.3f"
set xlabel "Packing fraction {/Symbol z}"

set output "plots/linear.pdf"
set format y "%.4f"
set ytics 0.0004
set xrange [0.274:0.288]
set yrange [-0.0008:0.0012]
plot y2(x) - y1(x) lc rgb "#777777",\
    file u 1:($6 - y1($1)):11 w yerrorbars ls 1

set output "plots/quadratic.pdf"
set ylabel "Compressibility difference {/Symbol D}Z_{MD} / 10^{–5}"
set format y "%.1f"
set ytics 1
set yrange [-5:5]
plot file u 1:( 1e5*($6-y2($1)) ):( 1e5*$11 ) w yerrorbars

set output "plots/cubic.pdf"
set ylabel "Compressibility difference {/Symbol D}Z_{MD} / 10^{–5}"
set format y "%.1f"
set ytics 1
set yrange [-5:5]
plot file u 1:( 1e5*($6-y3($1)) ):( 1e5*$11 ) w yerrorbars

set key top left invert

set output "plots/pressure-fit.pdf"
set ylabel "Compressibility Z_{MD}"
set format y "%.2f"
set ytics 0.05
set autoscale y
set label 1 sprintf("Z_{MD} = %.4f {/Symbol z}^2 %+.4f {/Symbol z} %+.5f", c2, b2, a2) \
    at 0.280,3.52
plot y2(x) lc rgb "#666666" t "Quadratic fit",\
    file u 1:6 w p ls 7 ps 0.25 t "Z_{MD}"

d0(x) = db0*x + da0
fit d0(x) d1_file u 1:2 via da0,db0
d1(x) = db1*x + da1
fit d1(x) d1_first u 1:2 via da1,db1
d2(x) = db2*x + da2
fit d2(x) d1_last u 1:2 via da2,db2

set output "plots/dzmd-dzeta.pdf"
set ylabel "First derivative of compressibility dZ_{MD} / d{/Symbol z}"
set ytics auto
set yrange[17.7:19.5]
set label 1 sprintf("Fit through all 43 points: dZ_{MD} / d{/Symbol z} = %.1f {/Symbol z} %+.2f", db0, da0) at 0.287,18.15 right
set label 2 sprintf("Fit through first 21 points: dZ_{MD} / d{/Symbol z} = %.1f {/Symbol z} %+.2f", db1, da1) at 0.287,18.0 right
set label 3 sprintf("Fit through last 21 points: dZ_{MD} / d{/Symbol z} = %.1f {/Symbol z} %+.2f", db2, da2) at 0.287,17.9 right

plot d0(x) lc rgb "#777777" t "Fit through all points",\
    d1_file w yerrorbars ls 1 t "dZ_{MD} / d{/Symbol z}"

