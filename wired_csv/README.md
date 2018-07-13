# wired_csv
My solution to the Wired CSV challenge was pretty simple. It looped through
the data file (given in it's compressed zip file) and found times when a key 
was pressed, after which it proceeded to find which bits were set at that specific time. 

It could be improved in runtime (currently on my 2013 Macbook Air it takes 208.056 seconds to run)
by storing the data table files in lists instead of rereading through the file each time.

Despite these performace issues, it does work and that's all I really cared about after spending way
longer than I'd like to admit reading through Atari 800 XLF documentation. Not to mention I gave it a
pretty awesome looking terminal output.
