tail -n 50000 /var/log/chrome/discoverability/discoverability.log |grep -v dataviz |grep -v "letsencrypt" |sed -rn "s/([^ ]+) - - \[([0-9]{2}\/[A-Za-z]+\/[0-9]+).*netflix\/watch.*/\1;\2/p"|grep -v "84.5.188.244" |grep -v "66." |grep -v "64\."|sed -rn "s/[^;]+;(.*)/\1/p"|sort|uniq -c|sed -rn "s/^ *(.*)/\1/p" > watches.csv
gnuplot ./watches.plg

