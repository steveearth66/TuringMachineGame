# Program to play the Turing Machine game, https://www.scorpionmasque.com/en/turingmachine
# forum at https://boardgamegeek.com/boardgame/356123/turing-machine
# by Steve Earth
# January 10, 2023

# 0th index is the Blue triangle, 1st index is yellow square, 2nd index is purple circle
# note that deck needs to be a list for comprehension, but must be recast as set for difference operations
deck = [(x,y,z) for x in range(1,6) for y in range(1,6) for z in range(1,6)]

#creating categories to slot possible responses. key = tuple of answer received, value = set of possible solutionss 
piles = {}
for i in range(2):
    piles[(i,)]=set([])
    for j in range(2):
        piles[(i,j)]=set([])
        for k in range(2):
            piles[(i,j,k)]=set([])

#encapsulating the comparison functions for easier coding
compare = [lambda x,y: x<y, lambda x,y: x==y, lambda x,y: x>y]

#L is a tuple, i in 1...5, count is how many i's and j's  are in L. did this rather than do length of a list filter
def count(L,i,j=None): #j is only used for check evens in cards 16,17 so this is a bit overkill
    ans=0
    for x in L:
        if x==i or x==j:
            ans+=1
    return ans

# class for the Verifier cards
class Verifier:
    def __init__(self,num, opts, sats=[]):
        self.num = num #this is the card number
        self.opts = opts # number of options on the card. redundant, but handy, as the len of sats
        self.sats = sats #list of sets of those tuple codes which satisfy the criteria for each option. 

''' for testing
    def __str__(self) -> str: 
        ans=""
        for i in range(self.opts):
            ans+="\nOption "+str(i+1)+" has "+str(len(self.sats[i]))+" members\n"
            ans+=str(self.sats[i])
        return "card num = "+str(self.num)+ans
'''

allVers = [0]*49 #initializing verifier deck. 0th index just a placeholder, in order to make it 1-indexed
#Card1: checking if blue is = or > 1
allVers[1] = Verifier(1,2,[{x for x in deck if x[0]==1},{x for x in deck if x[0]>1}])
#Cards2-3: checking if blue[yellow] is <=> 3
for j in [2,3]:
    allVers[j] = Verifier(j,3,[{x for x in deck if compare[i](x[j-2],3)} for i in range(3)])
#card4: yellow <=>4
allVers[4] = Verifier(4,3,[{x for x in deck if compare[i](x[1],4)} for i in range(3)])
#cards5-7: blue/yellow/red is even/odd
for j in [5,6,7]:
    allVers[j]=Verifier(j,2,[{x for x in deck if x[j-5]%2==i} for i in [0,1]])
#cards8-10: the number of 1/3/4 in the code (four options: 0,1,2,3)
for j in [8,9,10]:
    allVers[j]=Verifier(j,4,[{x for x in deck if count(x,[1,3,4][j-8])==i} for i in range(4)]) #using count function since ilst comprehension below buggy
    # allVers[j]=Verifier(j,4,[[x for x in deck if len([y for y in x if x==[1,3,4][j-8]])==i] for i in range(4)]) put everything in 1st slot, others empty?
#cards11-13: comparing blue/yellow to {yellow/purple}/purple
for j in range(3):
    allVers[j+11]=Verifier(j+11,3,[{x for x in deck if compare[i](x[[0,0,1][j]],x[[1,2,2][j]])} for i in range(3)])
    #considered comparing x[j(j-1)/2] to x[(3j-j*j+2)/2], but seemed obtuse vs [001][j] & [122][j]
#cards14-15: checks which color is smallest[largest]
for j in range(2):
    allVers[j+14]=Verifier(j+14,3,[{x for x in deck if compare[2*j](x[i],x[(i+1)%3]) and compare[2*j](x[i],x[(i+2)%3])} for i in range(3)])
#card16: evens > < odds. 
allVers[16]=Verifier(16,2,[{x for x in deck if compare[2-2*i](count(x,2,4),i+1) } for i in range(2)])
#card17: amt of evens
allVers[17]=Verifier(17,4,[{x for x in deck if count(x,2,4)==i} for i in range(4)])
#card18: sum is even/odd
allVers[18]=Verifier(18,2,[{x for x in deck if sum(x)%2==i} for i in range(2)])
#card19: blue+yellow <=> 6
allVers[19]=Verifier(19,3,[{x for x in deck if compare[i](x[0]+x[1],6)} for i in range(3)])
#card20: if code has a triple/double/no reps
allVers[20]=Verifier(20,3,[{x for x in deck if len(set(x))==i+1} for i in range(3)])
#card21: a number present exactly twice. 
allVers[21]=Verifier(21,2,[allVers[20].sats[0].union(allVers[20].sats[2]), allVers[20].sats[1]])
#card22: strictly ascending/descending/neither
allVers[22]=Verifier(22,3,[{x for x in deck if compare[2*i](x[0],x[1]) and compare[2*i](x[1],x[2])} for i in range(2)])
allVers[22].sats.append(set(deck) - allVers[22].sats[0]-allVers[22].sats[1])
#card23: sum < = > 6
allVers[23]=Verifier(23,3,[{x for x in deck if compare[i](sum(x),6)} for i in range(3)])
#card24: amt of successors. that is,  x,x+1 adjacent. 
allVers[24]=Verifier(24,3,[{x for x in deck if count([x[2]-x[1],x[1]-x[0]],1)==i} for i in range(2,-1,-1)])
#card25: same as card24 but also includes descending option. note: reversing symmetric tuples not duplicated due to sets
allVers[25]=Verifier(25,3,[allVers[24].sats[i].union({x[::-1] for x in list(allVers[24].sats[i])}) for i in range(3)])
#cards26-27 is a specific color < 3[4]
for i in [26,27]:
    allVers[i]=Verifier(i,3,[{x for x in deck if x[j]<[3,4][i-26]}for j in range(3)])
#cards28-30: is a specific color = [134]
for i in [28,29,30]:
    allVers[i]=Verifier(i,3,[{x for x in deck if x[j]==[1,3,4][i-28]}for j in range(3)])
#cards31-32 is a specific color > 1[3].  note: could have been merged with cards#26-27, but then code harder to read
for i in [31,32]:
    allVers[i]=Verifier(i,3,[{x for x in deck if x[j]>[1,3][i-31]}for j in range(3)])
#card33 = a specific color is even/odd. first card with multiple rows. opts read across then down: 012 \n 345
allVers[33]=Verifier(33,6, [{x for x in deck if x[i%3]%2==i//3} for i in range(6)])
#card34-35 = a specific color is the min[max] (allows ties)
for i in range(2):
    allVers[i+34]=Verifier(i+34,3,[{x for x in deck if x[j]==[min,max][i](x)} for j in range(3)])
#card36=sum is mult of 3/4/5
allVers[36]=Verifier(36,3,[{x for x in deck if sum(x)%(i+3)==0} for i in range(3)])
#cards37-38 are two specific colors summing to 4[6]
for i in range(2):
    allVers[i+37]=Verifier(i+37,3,[{x for x in deck if x[[0,0,1][j]]+x[[1,2,2][j]]==[4,6][i]} for j in range(3)])
#card39 = specific color compared to 1. reading across left-to-right then top-to-bottom on card: 012 \n 345
allVers[39]=Verifier(39,6, [{x for x in deck if compare[i//3+1](x[i%3],1)} for i in range(6)])
#card40-41 specific color compared to 3[4]. the first 9 option card
for i in range(2):
    allVers[i+40]=Verifier(i+40,9, [{x for x in deck if compare[j//3](x[j%3],[3,4][i])} for j in range(9)])
#card42= specific color is least or most
allVers[42]=Verifier(42,6,[{x for x in deck if compare[2*(i//3)](x[i%3],x[(i+1)%3]) and compare[2*(i//3)](x[i%3],x[(i+2)%3])} for i in range(6)])
#cards43-44: blue[yellow] compared to another color
for i in range(2):
    allVers[i+43]=Verifier(i+43,6,[{x for x in deck if compare[j%3](x[i],x[[[1, 0],[2,2]][j//3][i]])} for j in range(6)])
#cards45-47: amt of [131] or [344]
for i in range(3):
    allVers[i+45]=Verifier(i+45,6,[{x for x in deck if count(x,[[1,3,1],[3,4,4]][j//3][i])==j%3} for j in range(6)])
#card48 = specific color compared to another specific color
allVers[48]=Verifier(48,9, [{x for x in deck if compare[j//3](x[[0,0,1][j%3]],x[[1,2,2][j%3]])} for j in range(9)])


# S is a set, L is a list of list of lists etc of sets. this function intersects S with every set
def deepIntersect(S,L):
    if L==[]: #shouldn't be necessary, but just in case
        return []
    if isinstance(L[0],set): # L is a flat list of sets with no nesting. 
        return [S.intersection(x) for x in L] #note: this means all depths must be uniform
    return [deepIntersect(S,x) for x in L]

# initialize multiverse (list of possible solutions indexed by option of each card)
def makeVerse(L):
    if len(L)==1:
        return allVers[L[0]].sats
    return [deepIntersect(x,makeVerse(L[1:])) for x in allVers[L[0]].sats]

# returns a list of all the singleton index locations of the verse V paired with their only tuple
def singVers(V):
    if V==[]:
        return []
    if isinstance(V[0],set): # just a single verifier
        return [[[i],list(V[i])[0]] for i in range(len(V)) if len(V[i])==1] # was ans+="["+str(i)+"] = "+str(len(V[i]))+"\n"
    L=[]
    for i in range(len(V)):
        for v in singVers(V[i]):
            v[0].insert(0,i)
            L.append(v)
    return L
    # was "\n".join(["\n".join([ "["+str(i)+"]"+x for x in strVers(V[i]).split("\n") if x!=""]) for i in range(len(V))])

# given a list of verifiers, hex, this returns a list of all possible legal targets and their states
def presolver(hex):
    V=[hex]
    for i in range(len(V[0])): #this loop drops one verifier to see if same deduction can be made
        V.append(V[0][:i]+V[0][i+1:])

#this triple nested loop removes those answers that had a redundant verifier
    S=[singVers(makeVerse(v)) for v in V]
    for i in range(1,len(S)):
        for p in S[i]:
            for q in S[0]:
                if p[0] == q[0][:i-1]+q[0][i:] and p[1]==q[1]:
                    S[0].remove(q)
    return S[0]

''' for testing
# for now, hard code in the verifiers used for each present game in rule booklet. later can have user input.
game = [[4,9,11,14],[4,9,13,17],[3,7,10,14],[3,8,15,16],[2,6,14,17],[2,7,10,13],[8,12,15,17],[3,5,9,15,16],[1,7,10,12,17],
[2,6,8,12,15],[5,10,11,15,17],[4,9,18,20],[11,16,19,21],[2,13,17,20],[5,14,18,19,20],[2,7,12,16,19,22],[21,31,37,39],
[23,28,41,48],[19,24,30,31,38],[11,22,30,33,34,40], [14,17,19,21,22]]

# display results for preset games
for j in range(len(game)):
    S = presolver(game[j])
    print(len({x[1] for x in S }),"targets for game",j+1,"with criteria =",game[j])
    for s in S:
        print(s[0],s[1])
    print()
'''

resp=input("enter a list of criteria numbers separated by spaces, hit enter button to exit: ")
while resp!="":
    L = [int(x) for x in resp.split()]
    #create all possible queries, which could be 1, 2, or 3 of the given criterion cards
    # NOTE: when asking multiple criterion, the order will be in the order the user entered. NOT dependent on answers received.
    query=[[x] for x in L] #singletons
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            query.append([L[i],L[j]]) # asking a pair of questions
            for k in range(j+1,len(L)):
                query.append([L[i],L[j],L[k]]) # asking all three (max) questions.

    S = presolver(L)
    print(len({x[1] for x in S }),"targets for criteria =",L)
    for s in S:
        print(s[0],s[1])
    print()
    resp=input("enter a list of criteria numbers separated by spaces, hit enter button to exit: ")

''' these are utility functions for future reference, e.g. when program plays moves
# flattens all tuples in a verse to a single set
def bigUnion(V):
    if V==[]:
        return {}
    if isinstance(V, set):
        return V
    return bigUnion(V[0]).union(bigUnion(V[1:]))

# outputs list of all index locations in verse V of the tuple t
def findSol(V,t):
    if V==[]:
        return []
    if isinstance(V[0],set): #single verifier
        return ["["+str(i)+"]" for i in range(len(V)) if t in V[i]]
    L=[]
    for i in range(len(V)):
        for x in findSol(V[i],t):
            L.append("["+str(i)+"]"+x)
    return L

from math import log as Log
from math import inf as Inf
# L is a list of integers. turns(L) is measurement of value (lower is better), but -1 is flag for no options. turns=0 is best possible
# this estimates the expected number of turns it would take to find the target by dividing equally into the given amt of piles
def turns(L):
    # first strip away 0's
    L = [x for x in L if x > 0]
    if L == []:
        return -1 # this means no options left
    b = len(L) # used for base, note that b>=1, need base to acct for different length
    if b == 1:
        return Inf # that means everything yields the same answer, so no new information.   
    tot = sum(L) #note: need to scale by total in order to compare different amounts
    return sum([x/tot * Log(x,b) for x in L])
'''