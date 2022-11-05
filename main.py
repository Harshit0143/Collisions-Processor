## we can define a comparison between nodes
## keep keys as list of time and index i so we can sort by keys
## we can keep updating velocity an dpositon list alos
## 
## _key stores time of collision 
## it is either positive (as x[i]'s are distinct at t = 0)
## or negative by our definition
## we treat -1 as infinite i.e they never collide


## PHYSICS, Getting Final velocities of 'bodies' after collision
## Have used '-1' as infinte (i.e. bodies don't collide)
def col_time(x1,x2,v1,v2,t1,t2): # given  aboslute time when bodies collide
    # 'i' was at position 'xi' at time 'ti' , i = 1,2
    time = -1
    if (v1-v2>0) :
        time = (x2-x1+v1*t1-v2*t2 )/ (v1-v2)       
    return time
def col_vel(m1,m2,v1,v2):
    return ((m1-m2)*v1 + 2*m2*v2) / (m1+m2),((m2-m1)*v2 + 2*m1*v1) / (m1+m2)

# IDEA -> In the min_heap ('self._data[]') store a '_node' prioritized 
# '_node' corresponding to object 'i' stores absolute time at which 'i' and 'i+1' collide , i = 0,1...n-2
# extract_min from the heap , edit the required parameters (explained later)
# then again put it in the heao with the new time for collision (-1)
class heap: # using list
    class _node: 
        __slots__=['_key','_num'] # for memory efficiency
        def __init__(self, time,i):
            self._key = time
            self._num=i
            ## we will sort by key, break tie in time by i  (see Problem Statement)

        
        # '-1' used as infinity i.e. time  = -1
        # means objects never collide 
        # se need to define the comparion in that way

        def __eq__(self, other):
            return self._key==other._key and self._num==other._num
        def __gt__(self,other):
            if (self._key==-1):
                if (other._key ==-1):
                    return self._num>other._num
                else:
                    return True
            elif (other._key==-1) :
                return False
            else: # none is -1
                if (self._key!=other._key):
                    return self._key>other._key
                else :
                    return self._num>other._num
        def __ge__(self,other):
            return self>other or self==other 
        def __lt__(self,other):
            return not self>=other
        def __le__(self,other):
            return not self>other   
         
        
        # 0-indexed almost complete binary tree
        # index parent  of node of index 'm' = (m-1)//2
        # l child of node of index 'n' = 2n+1
        # r child of node of index 'n' = 2n+2

    # Bodies  A->   B-> <-C D->   Before collision
    #         A->   <-B C-> D->   After B and C collide
    #  Now, velocities of 'A' and 'D' are unchanged, but collision time 'A' with 'B'
    # and 'C' with 'D' changes so we need to EDIT the '_node' of 'A' and 'C' in the heap
    # how do we do that? We don't want to search the entire heap
    # The list L[] (size = n-1) helps
    # L[i] = index of '_node' of object 'i' 0<= i<= n-2 
    # (object n-1 isn't required as it as no one to colide to on the right)
    # We update L[] dynamically when whenever we do any operations on the heap

    # X[i] is the position of the body 'i'  on the number line
    # after a collision, we wish to update the X[i] if we need to store the positions of all 'bodies' at the same time
    # but that will take O(n) time
    # instead we maintain an array last[] that stores the 'time' when position of 'i' was last updates
    # hence position of 'i' is X[i] at time last[i]
    # we will update last[i] and X[i] only when 'i' collides
    # in between that, the velocity of 'i' is constant so we can calculate it's position easily

    
    def __init__(self,times,L):
        self._size= len(times)
        self._data = [None]*self._size 
        for i in range (self._size-1 , -1,-1):
            L[i]=i
            self._data[i]=self._node(times[i],i) # the fast build heap method (filling down to up)                                     
            self.heap_down(i,L)                  # takes O(n) time BETTER than O(nlog(n))
    
    def __len__(self):
        return self._size
    
    def root_info(self):
        return self._data[0]._key , self._data[0]._num 

    def heap_up(self,id ,L): # takes list index to heap up
        while (id-1)//2 >= 0 :
            par = (id-1)//2 
            if self._data[par] <= self._data[id]: # we defined the comparison b/w node ojects earlier
                break
            L[self._data[id]._num] =  par # Updating L[]
            L[self._data[par]._num] = id
            self._data[id] , self._data[par]= self._data[par],self._data[id]
            id=par
        return id
    def heap_down(self,id,L):
        l_id = len(self)-1
        while (2*id + 1 <= l_id ):
            l_ch = 2*id + 1 
            r_ch = 2*id + 2
            min_ch = l_ch
            if r_ch<= l_id: 
                if self._data[r_ch] <= self._data[l_ch]:
                    min_ch = r_ch
            if self._data[min_ch]>= self._data[id]:
                break
            L[self._data[id]._num] =  min_ch  # Updating L[]
            L[self._data[min_ch]._num] = id 
            self._data[id] , self._data[min_ch]= self._data[min_ch],self._data[id]
            id=min_ch
       
    def change_time(self, id, time_new,L): # editing the '_node' of neighbours in the heap
        old_node =   self._node(self._data[id]._key,self._data[id]._num)
        self._data[id] = self._node(time_new,self._data[id]._num)
        if (old_node>self._data[id]):
            self.heap_up(id,L)
        else :
            self.heap_down(id,L)

## we will keep modifying X and V in place

def listCollisions(M,X,V,m,T): #    M[]-> masses, X[] -> initial positoinss (x[i]< x[i+1]), V[i]-> initial velocities
    # 'm' -> Report only first 'm' collisions or T-> collisions till time 'T' whichever is less
    ans = []
    n = len(M)
    L =[] # in it we will store L[i] = index in heap of xi 
    # allows to access stats of neighbours in O(1) time
    for i in range (0,n-1):
        L.append(i)
    last = [0]*n
    times = []
    # building the heap
    for i in range (0,n-1):        
        times.append(col_time(X[i],X[i+1],V[i],V[i+1],0,0))
    h = heap(times,L)


    while len(ans)<m :
        now_time , i = h.root_info()
        if (now_time==-1 or now_time>T): # we are including the collision that happens at time T
            break
        X[i]=X[i+1]= X[i]+V[i]*(now_time-last[i])
        ans.append( (now_time,i,X[i]))
        
        last[i]=last[i+1]=now_time   
        V[i] , V[i+1] = col_vel(M[i],M[i+1],V[i],V[i+1])
        h.change_time(0,-1,L)
        # A->  B-> <-C D->  and B & C collide 
        if (i>0):  # editing _node of 'A' if 'A' exists
            loc_prev = L[i-1]
            h.change_time(loc_prev,col_time(X[i-1],X[i],V[i-1],V[i],last[i-1],last[i]),L)
           
        if (i<=n-3):  # editing '_node' of 'C' if it's not the rightmost body
            loc_next = L[i+1]
            h.change_time(loc_next,col_time(X[i+1],X[i+2],V[i+1],V[i+2],last[i+1],last[i+2]),L)
    return ans
        
# print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
# print(listCollisions([100000.0, 1.0, 100000.0, 1.0, 100000.0], [0.0, 10.0, 20.0, 30.0, 40.0], [0.0, -2.3, 0.0, -2.5, 0.0], 100,100.0))  
# print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
# print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))