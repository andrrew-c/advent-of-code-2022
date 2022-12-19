# Advent of code - 2022 
Andrew Craik's attempts.

Wish me luck!

## Jump to:
- [Day 1 - Calorie carrying Elves](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-1-calorie-carrying-reindeer)
- [Day 2 - Rock, paper and scissors](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-2-rock-paper-and-scissors)
- [Day 3 - Rucksacks of strings](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-3-rucksacks-of-strings)
- [Day 4 - Camp cleanup](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-4-camp-cleanup)
- [Day 5 - Supply Stacks](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-5-supply-stacks)
- [Day 6 - Tuning Trouble](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-6-tuning-trouble)
- [Day 7 - No Space Left On Device](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-7-no-space-left-on-device)
- [Day 8 - Treetop Tree House](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-8-treetop-tree-house)
- [Day 9 - Rope Bridge](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-9-rope-bridge)
- [Day 10: Cathode-Ray Tube](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-10-cathode-ray-tube)
- [Day 11: Monkey in the Middle](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/tree/andrewc-2022/andrewc_2022#day-11-monkey-in-the-middle)
- [Day 12: Day Hill Climbing Algorithm](https://github.com/moj-analytical-services/ds-risk-team-adventofcode/blob/andrewc-2022/andrewc_2022/README.md#day-12-hill-climbing-algorithm)
- [Day 13: Distress Signal]()
- [Day 14: Regolith Reservoir]()
## Day 1: Calorie Counting

To run this code enter `python andrewc/day1_andrewc.py`

### Part 1: What is the largest amount carried by one?

I attempted this using a `for` loop and `groupby` to see if one was quicker
Results are printed out

### Part 2: Total amount carried by the 3 largest

Went for the quickest solution I could fine

## Day 2: Rock Paper Scissors

To run this code enter `python andrewc/day2_andrewc.py`

### Part 1: Work out score based on being told what to play

Rock paper or scissors and calculate score.

### Part 2: Work out score based on being told how to end game

Work out result of game, what shape you need (rock,etc.) then calcualte score in same way as part 1.

## Day 3: Rucksack Reorganization

To run this code enter `python andrewc/day1_andrewc.py`

### Part 1: Calculate common string 
Map to score and sum up

### Part 2: Group up each rucksack in 3s

## Day 4: Camp Cleanup

### Part 1: Calculate ranges that overlap

Find the ranges which overlap entirely - use `set`.

### Part 1: Calculate ranges that overlap (at all)

Using `set` again - checking for any common values

## Day 5: Supply Stacks

### Part 1: Crate moves them one by one

Found reading the data in quite tricky.  Alternatives I thought of included specifying column widths (a la 'fixed width format').
Added elements one by one in a loop - could probably do in one step, but was creating multi-dimensional lists.  Solution could have been to flatten it, but I was getting bored.

## Part 2: Crate can move multiple

Simple change in logic to reverse the items.  I noticed  my code was modifying the input dictionary, but couldn't see where it was going wrong.

## Day 6: Tuning Trouble

### Part 1: Check for unique characters where packet size = 4

For once, found this very quick.  Wondered if this could be solved through recursion (rather than a loop), but think this might cause problems with how 'deep' you can go.

## Part 2: Same as part 1 - where packet size = 14

Created a function from part 1 and modified it.

## Day 7: No Space Left On Device

Original note: OMG, this was a nightmare. I won't give up.
OK - my mistake was to try and solve this through nested dictionaries.  
Only once I thought of using a class (following more difficult puzzles in later days) did I realise it would make sense for this.

### Part 1: Sum total of folders < 10000

Worked out that a global class property (`all_folders`) would make this easier.

### Part 2: Smallest folder to delete that will free up enough space for update

Was quick - due to way I solved this (eventually.)

## Day 8: Treetop Tree House

Going to see if I can do this quicker.
Using loops and list comprehension.
Realised I could slice the arrays and remove the one element.

Part 2 involved some changes, and I later realised I needed to reverse the 'up' and the 'left' slice.

## Day 9: Rope Bridge

### Part 1: Head must be touching

I've probably over engineered this solution but wasn't sure how else to approach.

I produced a class object called 'Knot' which has X,Y coords
and some other methods including 'am i touching' or 'move me towards'.

Though this was quite a complicated solution, I got the answer right first time, which was unusual for me! 

### Part 2: 

Glad I went with Class objects - was quite easy to update to extend the number of knots.

## Day 10: Cathode-Ray Tube

### Part 1: What is the sum of these six signal strengths?

Nearly went with loops but realised I could implement with a dataframe where the cycles jump 1, 4, 6, 8, 9, 10, etc.

I then merge on a complete set of 'cycles' and use forward fill to complete 'missing' cycles.

### Part 2: Render the image

## Day 11: Monkey in the Middle

### Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?

### Part 2: No worry reduction

Gave up on this, for now....

## Day 12: Hill Climbing Algorithm

### Part 1: Fewest steps

What is the fewest steps required to move from your current position to the location that should get the best signal?

### Part 2: 

## Day 13: Distress Signal

## Day 14: Regolith Reservoir

## Day 15: Beacon Exclusion Zone

## Day 16: Proboscidea Volcanium

## Day 17: Pyroclastic Flow