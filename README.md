# Collisions-Processor

# Problem Statement
Consider a set of 'n' point objects located in 1D space where for i ∈ {0, . . . , n − 1} <br/> 

Given this initial conditions, the objects undergo several collisions over time and eventually move away from one another.<br/> 

# 
Assume that each collision is elastic, and therefore, kinetic energy is conserved too. Also, note that no two objects can ever “cross” each other, and therefore, collisions can happen only between objects i and i + 1, for some i ∈ {0, . . . , n − 2}.<br/> 
# Tie-Breaking
We represent a collision by a tuple of a real number, an integer, and another real number. The tuple (t, i, x) represents a collision happening at time t between objects i and i + 1 at location x.<br/> 

Our goal is to enumerate the resulting collisions in a chronological order. Ties between collisions happening at the same time must be broken from left to right. For example for i < i′, if at time t, object i collides with i + 1 at location x, and i′ collides with i′ + 1 at location x′, then the collision (t, i, x) must precede (t, i′, x′). <br/> 

#ASSUMPTION: 
Input is such that no more than 2 objects collide at the same time and the same place.<br/> 
 

1. M[]: a list of positive floats, where M[i] is the mass of the i’th object, <br/> 
2. X[]: a sorted list of floats, where x[i] is the initial position of the i’th object,<br/> 
3. V[]: a list of floats, where v[i] is the initial velocity of the i’th object,<br/> 
4. m: a non-negative integer,<br/> 
5. T: a non-negative float,<br/> 

returns a list of collisions in chronological order that ends as soon as the first m collisions happen or time reaches T (whichever earlier). <br/> 
If the input results in fewer than m collisions and the last collision happens before time T, the list returned must contain all collisions in chronological order.


# Example Test Cases
listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0) <br/> 
[]<br/> <br/> 
listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5,5.0)<br/> 
[(1.0, 0, -2.0), (1.0, 2, 2.0)]<br/> <br/> 
listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0)<br/> 
[(1.0, 1, 1.0), (1.505, 0, 0.0), (1.6756, 1, 0.3377), (1.7626, 0, -0.0001), (1.8163, 1,
 0.2080), (1.8533, 0, -0.0002)]<br/> <br/> 

listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5)<br/> 
[(1.0, 1, 1.0)]<br/> <br/> 
