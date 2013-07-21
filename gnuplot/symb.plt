# Setting the terminal postscript with the options
set terminal postscript eps color enhanced "Helvetica" 20

# Setting the output file name
set output 'plot.eps'

#Setting up the grid and labels
set grid
set title "A simple graphic without LaTeX"
set xrange [-pi:pi]
set xlabel "Angle {/Symbol a}"
set ylabel "{/Symbol Dw}"
set ytics 0.5
set xtics ("{/Symbol p}" -pi, "{/Symbol p}/2" -pi/2, "0" 0, "{/Symbol p}/2" pi/2, "{/Symbol p}" pi)

# Setting the legend
set key horizontal below height 2
set key box lt 2 lc -1 lw 3

# The plot itself (\ is to broke lines)
set size 1,1
plot sin(x)**2 w l lt 1 lc 1 lw 3 t "sin^2({/Symbol a})", \
sin(2*x)/x w l lt 2 lc 3 lw 3 t "sin(2{/Symbol a})/{/Symbol a}", \
sin(x) w l lt 3 lc 2 lw 3 t "sin{/Symbol a})"
