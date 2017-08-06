set terminal pngcairo size 3600,2400
set output "phagecolicin_assay_log.png"

set multiplot
set tics front
set border 15 lw 2 lc rgb "#2e3436"

set xra [0:24]
set xtics 6
set yra [1e-3/1.2:1.2e1]
set logscale y
set format y "10^{%L}"
# set ytics .5
# set mytics 5

xsize = 1/12.
ysize = 1/8.

xoffset = 0
yoffset = 0

set size xsize*1.07,ysize*1.05
unset key

set grid
do for [i=0:11] {
    do for [j=0:7] {
        set label 1 sprintf("t_{add} = %d min",j*30) at graph .5,.9 center front
        set arrow 1 from .5*j,graph 0 to .5*j,graph 1 nohead lw 2 lc rgb "#f57900" back
        set origin i*xsize+xoffset,(7-j)*ysize+yoffset
        col = j + i*8 + 3
        plot "out" u 1:col w p pt 7 ps .3 lc rgb "#3465a4"
    }
}


