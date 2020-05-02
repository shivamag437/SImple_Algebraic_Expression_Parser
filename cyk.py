grammar={"Start":["HT","IT","JF","KF","0","1","2","3","4","5","6","7","8","9","AB"],"E":["HT","IT","JF","KF","0","1","2","3","4","5","6","7","8","9","AB"],"T": ["JF","KF","0","1","2","3","4","5","6","7","8","9","AB"], "F": ["0","1","2","3","4","5","6","7","8","9","AB"], "A":["("], "B":["ED"], "D":[")"], "H":["EP"], "P":["+"], "I": ["EQ"], "Q":["-"], "J":["TR"], "R":["/"], "K":["TX"], "X":["*"]}   
#grammar={'S':["AB","BC"],"A":["BB","0"],"B":["BA","1"],"C":["AC", "AA", "0"]}
print("Enter your string")
w=input()
length=len(w)+1

#array where we will store our non-terminals that give a production in our grammar
arr= [[0 for i in range(length)] for j in range(length)]

#forms the first line in the table where at the position for each terminal, we enter the non-terminals that can derive that production
for i in range(1,length):
	singlecharacter=w[i-1]
	savelist=[]
	for key in grammar:
		for j in range(0,len(grammar[key])):
			#print(grammar[key][j],singlecharacter)
			if(grammar[key][j]==singlecharacter):
				savelist.append(key)
	arr[1][i]=savelist			
#print(arr)

#this functions finds all the permutations in which we can divide our string. So if x=5, it returns a list=[[1,4][2,3],[3,2],[4,1]]
def calculatepermutations(x):    
	listofper=[]
	for i in range(1,x):
		listofper.append([i,x-i])
	return(listofper)

#this entire nested for loop fill up the table in a botton to top manner
cc=length-2
for i in range(2,length):
	for j in range(1,length):
		if(j<=cc):
			lookahead=i
			newlistofrules=[]
			permutations=calculatepermutations(i)
			#print(permutations)
			for a in range(0,len(permutations)):
				index1,index2=permutations[a]
				block1=arr[index1][j]
				#print(index2, " hello", " i",index1,j )
				block2=arr[index2][index1+j]

				#print(block1,block2)
				if(block1!="NIL" and block2!="NIL"):
					for k in range(0,len(block1)):
						for l in range(0,len(block2)):
							possibleproductin=block1[k]+block2[l]
							#print("production",possibleproductin)
							for key in grammar:
								for q in range(0,len(grammar[key])):
									if(grammar[key][q]==possibleproductin):
										#print(key)
										newlistofrules.append(key)
			#print("i and j are",i,j)
			if(newlistofrules==[]):
				arr[i][j]="NIL"
			else:
				arr[i][j]=list(set(newlistofrules))
	cc=cc-1

# print("The table is :")
#print(arr)

accept=0
for r in range(0,len(arr[length-1][1])):
	if(arr[length-1][1][r]=="Start"):
		accept=1
		print("\nThe string ",w, " is accepted")

if(accept==0):
	print("\nThe string is not accepted")

