#============= AoC Env functions =============#
# These functions can be added to the activate
# script(s) so that it's easier to jump into
# AoC problems
#=============================================#

# AoC newday command
newday () {
    python /Users/work/dev/AoC2023/newday.py $1
}

# AoC runday command
runday () {
    if [ "$1" != "" ]
    then
        AoCDIR=$(printf "%02d" $1)
        echo "Running Day$AoCDIR"
        python /Users/work/dev/AoC2023/Day$AoCDIR/Day$AoCDIR.py > /Users/work/dev/AoC2023/Day$AoCDIR/Day$AoCDIR.out
    else
        local AoCDIR=$(print -l Day[0-9][0-9](/N) 2> /dev/null | tail -n 1)
        if [[ -n $AoCDIR ]]; then
            echo "Running $AoCDIR"
            python /Users/work/dev/AoC2023/$AoCDIR/$AoCDIR.py > /Users/work/dev/AoC2023/$AoCDIR/$AoCDIR.out
        else
            echo "No 'DayXX' directories found."
        fi
    fi
}
