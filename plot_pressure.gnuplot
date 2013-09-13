#!/usr/bin/gnuplot
set terminal pdf enhanced color dashed

system("[ -f fit.log ] && rm fit.log")

set datafile separator "\t"
file = "csv/uniform.csv"

a1 = -1.64
b1 = 18.7
y1(x) = b1*x + a1
fit y1(x) file u 1:6 via a1,b1

a2 = 2.85
b2 = -13.3
c2 = 56.9
y2(x) = c2*x**2 + b2*x + a2
fit y2(x) file u 1:6 via a2,b2,c2

unset key
set format x "%.3f"
set xlabel "Packing fraction n"
set ylabel "Pressure difference {/Symbol D}p"

set output "plots/linear.pdf"
set title sprintf("Differential plot of a linear fit: p = %.2f n %+.2f", b1, a1)
set format y "%.4f"
set ytics 0.0004
set xrange [0.274:0.288]
set yrange [-0.0008:0.0012]
plot y2(x) - y1(x) lc rgb "#777777",\
    file u 1:($6 - y1($1)):11 w yerrorbars ls 1

set output "plots/quadratic.pdf"
set ylabel "Relative pressure difference {/Symbol D}p / p / 10^{–6}"
set title sprintf("Differential plot of a quadratic fit: p = %.2f n^2 %+.2f n %+.2f", c2, b2, a2)
set format y "%.1f"
set ytics auto
set autoscale y
plot file u 1:( 1e6*($6-y2($1))/$6 ):( 1e6*$11/$6 ) w yerrorbars

set key bottom right

set output "plots/pressure-fit.pdf"
set title "Computed pressure values"
set ylabel "Pressure p"
set format y "%.2f"
set ytics 0.05
plot y1(x) lc rgb "#ff7777" t "linear fit",\
    y2(x) lc rgb "#7777ff" t "quadratic fit",\
    file u 1:6:11 w yerrorbars ls 1 t "pressure"
