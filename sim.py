import csv
import random
import statistics
import math

# Function to create the pool of champions
## pool is the list where the pool will be created
## tft_tiers_char_number is the matrix with the number of character by tiers
## tft_tiers_copies is the matrix with the number of copies of characters by tiers
def creatingPool(pool, tft_tiers_char_number, tft_tiers_copies):
    for i in range(len(tft_tiers_char_number[0])):
        tier_i = []
        for j in range(tft_tiers_char_number[1][i]):
            tier_i.append(tft_tiers_copies[1][i])
        pool.append(tier_i)

# Function that returns a particular shop of 5 characters, extracted from the pool
## pool is the current pool of characters (which will be modified to extract some)
## tft_tiers_prob is the matrix of the probability of each tier by level
## level is the current level of the player buying
def get_a_roll(pool, tft_tiers_prob, level):
    prob_tier = [float(k) for k in tft_tiers_prob[level-1][1:]]
    tiers_name = [int(k) for k in tft_tiers_prob[0][1:]]

    roll = []
    for i in range(5):
        tier = random.choices(tiers_name, prob_tier)[0]
        pool_tier = pool[tier-1]
        n_char = random.choices(range(len(pool_tier)), pool_tier)[0]
        pool[tier-1][n_char] = pool[tier-1][n_char]-1
        roll.append([tier, n_char+1, 1])
    return(roll)

# Returns the characters that haven't been bought to the pool
## pool is the current pool of characters
## roll is the state of the shop/roll that we want to return to the pool
def return_a_roll(pool, roll):
    for (tier, n_char, in_roll) in roll:
        if(in_roll == 1):
            pool[tier-1][n_char-1] = pool[tier-1][n_char-1]+1

# We need to open the three csv with basic data of the game

csv_file = open('tft_tiers_prob.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
tft_tiers_prob = []
for row in csv_reader:
    r = []
    for cell in row:
        r.append(cell)
    tft_tiers_prob.append(r)

csv_file = open('tft_tiers_char_number.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
tft_tiers_char_number = []
for row in csv_reader:
    r = []
    for cell in row:
        r.append(int(cell))
    tft_tiers_char_number.append(r)

csv_file = open('tft_tiers_copies.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
tft_tiers_copies = []
for row in csv_reader:
    r = []
    for cell in row:
        r.append(int(cell))
    tft_tiers_copies.append(r)

# We create the initial pool of characters
pool = []
creatingPool(pool, tft_tiers_char_number, tft_tiers_copies)

# We want to make a simulation about the shop when nobody has bought anything
# The question being asked is: "How many rerolls do we need to buy a particular
# character X times if we're at level Y and the character is of tier T?"
# The number of times we want to buy the character is on total_to_buy,
# after that I do a table of the average of rerolls for the rerolls for each level/tier (Y/T)

n_sim = 1000    # Number of "matches" to try. Higher means better precision and longer execution time
total_to_buy = 3 # Number of times we want to buy this particular champion in each tier / level


s = 0
results = []
for level in range(2,10):
    avg_rolls = []
    for tier in range(1,6):
        iterations = []
        for k in range(n_sim):
            pool = []
            creatingPool(pool, tft_tiers_char_number, tft_tiers_copies)
            bought = 0
            n_rolls = -1 # We start at -1 because the first roll is free, no need to count that
            if(math.isclose(float(tft_tiers_prob[level-1][tier]),0)):
                n_rolls = -1 # It's impossible to obtain in this level, -1 means infinite rolls
            else:
                while(bought < total_to_buy):
                    n_rolls = n_rolls+1
                    roll = get_a_roll(pool, tft_tiers_prob, level)
                    for i in range(len(roll)):
                        if((roll[i][0] == tier) and (roll[i][1] == 1)):
                            bought = bought+1
                            roll[i][2] = 0
                    return_a_roll(pool, roll)

            iterations.append(n_rolls)
        avg_rolls.append(statistics.mean(iterations))
    results.append(avg_rolls)
print(results)

# Uncomment this if you want the results in a csv

#with open('results.csv', mode='w') as results_file:
#    results_csv = csv.writer(results_file)
#
#    for r in results:
#        results_csv.writerow(r)
