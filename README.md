# Annotate-Sequence-Reads
This repro contains my solution to a practice bioinformatic coding challenge. My solution to this challenge is fast (under 10s for 100,000 annotations), simple, and easily modifiable. Overall, my solution recieved high praise for speed and robustness. 

## The challenge: 
Given a file of sequence reads that includes the chromosome and the postition-coordinate of a read within that chromosome, write a program for looking up its annotation within a seperate GTF file.  

Input:
    
    o	Tab-delimited file: Chr<tab>Position
    
    o	GTF formatted file with genome annotations.
Dedired Output: 
		
    o	Annotated file of gene name that input position overlaps.
