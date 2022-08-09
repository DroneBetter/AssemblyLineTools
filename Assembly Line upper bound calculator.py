import math

raws=["copper","gold","iron","diamond","aluminium"] #and wriggling
processed=["liquid","gear","wire","plate"]
itemNames=raws+[i+" "+j for j in processed for i in raws]
itemNames+=["circuit","engine","heater plate","cooler plate","light bulb","clock","antenna","grill","toaster","air conditioner","battery","washing machine","solar panel","headphones","processor","drill","power supply","speakers","radio","jackhammer","TV","smartphone","fridge","tablet","microwave","railway","smartwatch","server rack","computer","generator","water heater","drone","electric board","oven","laser","advanced engine","electric generator","super computer","electric engine","AI processor","AI robot body","AI robot head","AI robot"]
vowels={"a","e","i","o","u"}
itemPlurals=[i[:-1]+"ies" if i[-1]=="y" and i[-2] not in vowels else i+"e"*(i[-2:]=="ch")+"s"*(i[-1]!="s") for i in itemNames]
machineNames=["starter","furnace","cutter","wire drawer","hydraulic press","crafter"]
itemMachines=[i for i in range(len(machineNames)) for j in range(len(raws))]
itemMachines+=[len(machineNames)-1]*(len(itemNames)-len(itemMachines))
itemRecipes=[[]]*len(raws)+[[i] for i in range(len(raws))]*len(processed)+   [[15,1],[12,11],[3,0,15],[3,1,16],[2,15],[2,1,10],[18,2],[27,2],[27,4,0],[28,1,4],[4,9,25],[26,4,0],[25,1,3],[25,16,18],[25,4],[3,10,26],[25,15,17],[25,16,18],[25,31,35],[25,3,22],[41,25,4],[39,35,4],[28,41,4],[39,35,4],[27,23,24],[2,22], [39,22,24],[24,4], [39,41,4],[26,20,21],[27,23,24],[35,39,24],[25,20,22],[27,20,22],[35,23,25],[26,25],[54,25,35],[53,52],[35,60],[62,25],[4,63,61],[64,4], [66,65]]
itemRecipeQuantities=[[1]]*len(raws)*(1+len(processed))+                     [[2,1], [2,1],  [1,1,1], [1,1,1], [2,2], [2,2,1], [4,1], [1,4], [1,1,1], [1,1,1], [1,1,1], [1,2,2], [1,2,1], [1,1,1],   [2,2], [2,2,1],  [1,3,3],   [2,4,4],   [1,1,1],   [4,4,4],  [1,1,4],  [1,1,2],  [1,1,6],  [1,1,4],  [1,5,5],   [10,10],[2,1,2],   [20,10],[1,1,6],  [4,5,5],   [5,5,5],   [2,2,4],   [20,6,6],  [10,10,10],[6,10,6],  [50,50],[15,50,40],[30,10],[40,10],[4,40], [400,1,1],[1,200],[1,1]]
itemPrices=[80]*len(raws)+[100]*len(raws)*(len(processed)-1)+[250]*len(raws)+[ 300,   360,    360,     360,     360,   540,     540,    600,  900,     900,     1050,    1100,    1170,    1300,      1320,  1500,     1920,      3300,      5670,      6920,     7100,     7300,     7400,     7600,     8070,      8400,   10170,     10600,  11000,    11820,     12900,     17220,     27000,     27300,     31800,     70000,  470000,    550000, 900000, 2500000,2800000,  5000000,15000000]
sumResourceCosts=[]
itemProcessingCosts=[]
#itemSpaceCosts=[]
itemStarterUpperBounds=[]
itemSpaceUpperBounds=[]
specificResourceCosts=[]
itemFractions=[]

def armRecipe(i,arm):
    recipe=itemRecipes[i]
    quantity=1
    for j in arm:
        (i,recipe,quantity)=(recipe[j],itemRecipes[recipe[j]],quantity*itemRecipeQuantities[i][j])
    return (recipe,quantity)
def squares(i,n):
    def proceedArm():
        if len(arm)>0:
            if arm[-1]+1<len(armRecipe(i,arm[:-1])[0]):
                arm[-1]+=1
                while len(armRecipe(i,arm)[0])>0:
                    arm.append(0)
            else:
                del arm[-1]
                proceedArm()
    arm=[]
    while len(armRecipe(i,arm)[0])>0:
        arm.append(0)
    rawDestinations=[0]*len(raws)
    while len(arm)>0:
        dest=i
        destQuan=n
        #print(arm)
        for j in arm:
            #print(dest,j,itemNames[dest],itemRecipes[dest],itemRecipeQuantities[dest])
            (formerDest,formerDestQuan)=(dest,destQuan)
            destQuan*=itemRecipeQuantities[dest][j]
            dest=itemRecipes[dest][j]
        if dest<len(raws):
            rawDestinations[dest]+=formerDestQuan
        proceedArm()
    rawStarters=[--0--(s*n)//3 for s in specificResourceCosts[i]]
    rawExceedings=[d-s for d,s in zip(rawDestinations,rawStarters)]
    return n*itemProcessingCosts[i]+spatialSumStarters[-1]*(n//m)+spatialSumStarters[n%m]+sum(--0--r//2 for r in rawExceedings)+--0--(n//3 if i<len(raws) else n)//4
for i,(m,r,q) in enumerate(zip(itemMachines,itemRecipes,itemRecipeQuantities)):
    if m==0:
        sumResourceCosts.append(1)
        itemProcessingCosts.append(0)
        #itemSpaceCosts.append(1/3)
        specificResourceCosts.append([int(k==i) for k in range(len(raws))])
    else:
        recipeSum=sum([u if itemMachines[e]==0 else --0--u//3 for e,u in zip(r,q)])
        sumResourceCosts.append(sum([u*sumResourceCosts[e] for e,u in zip(r,q)]))
        itemProcessingCosts.append(sum([u*itemProcessingCosts[e] for e,u in zip(r,q)])+1)
        #itemSpaceCosts.append(1+(2/3 if m!=5 else sum([u*itemSpaceCosts[e]+(itemMachines[e]==0)*(u%3)/3 for e,u in zip(r,q)])+int(recipeSum>3)*--0--(recipeSum-3)//2)) #a single raw item in a recipe requires 1/3rd of a splitter and starter, two require 2/3rds of each (because three require two of each), three requires a splitter and no starters, so splitter cost is (raws%3)/3. In the upper bound case, if an item requires more than 3 ingredients, there are no optimisations where two itemNames' excess rollers can be substituted for a single two-way splitter, because it would require having one input per output, while rollers need at least two to be worth having. If an item has raw materials in its recipe, it can use four inputs instead of three and output to the starter (to be picked up by a robot arm) but this requires 1/2 seconds output rate and uses an additional square regardless, so doesn't need to be considered in upper limits
        specificResourceCosts.append([sum([u*specificResourceCosts[e][k] for e,u in zip(r,q)]) for k in range(len(raws))])
    '''m=1
    while not all((k*m)%3==0 for k in specificResourceCosts[i]):
        m+=1''' #can never be 2 (think about it)
    m=3**any(k%3!=0 for k in specificResourceCosts[i])
    spatialSumStarters=[sum(--0--(s*n)//3 for s in specificResourceCosts[i]) for n in range(1,m+1)] #for spatial upper bound purposes
    (upperBound,remainingStarters)=divmod(56,(sumResourceCosts[i]*m/3))
    upperBound=int(upperBound*m)
    typesInItem=sum(k>0 for k in specificResourceCosts[i])
    if typesInItem<=remainingStarters:
        remainingStarters-=typesInItem
        remainingCosts=[k-3*(k>0) for k in specificResourceCosts[i]]
        bottleneckValue=1
        while remainingStarters>=0:
            bottleneckIndex=-1
            bottleneckValue=0
            for k,(r,s) in enumerate(zip(remainingCosts,specificResourceCosts[i])):
                if s>0:
                    value=r/s
                    if bottleneckIndex==-1 or value>bottleneckValue or (value==bottleneckValue and s<specificResourceCosts[i][bottleneckIndex]):
                        bottleneckIndex=k
                        bottleneckValue=value
                        fraction=[s-r,s]
            if bottleneckValue<=0:
                upperBound+=1
                for k in range(len(remainingCosts)):
                    remainingCosts[k]+=specificResourceCosts[i][k]
            else:
                if remainingStarters>=0: #the one at 0 is only to recalculate the bottleneck without duplicate code (delightfully devilish, Seymour)
                    if remainingStarters>0:
                        remainingCosts[bottleneckIndex]-=3
                    remainingStarters-=1
        upperBound+=1-bottleneckValue
        gcd=math.gcd(fraction[0],fraction[1])
        itemFractions.append([int(j/gcd) for j in fraction])
    else: #it's over
        itemFractions.append([0,1])
    itemStarterUpperBounds.append([3*56/sumResourceCosts[i],upperBound])
    itemFractions[i][0]+=math.floor(upperBound)*itemFractions[i][1]
    upperBound=0
    squaresUsed=0
    while squares(i,upperBound+1)<=256: #assuming utilisation of all four sides of sellers
        upperBound+=1
    upperBound+=1 #because it only works with integers currently so is providing an upper bound on the upper bound instead of a lower bound on it
    itemSpaceUpperBounds.append(upperBound)

indentation=len(str(len(itemRecipes)))

def itemReport(i,recipe,value,cost,specific,starterUpperBound):
    print(" "*(indentation-len(str(i+1)))+str(i+1)+". "+itemNames[i]+recipe*(": "+str([str(itemRecipeQuantities[i][j])+" "+itemNames[itemRecipes[i][j]] for j in range(len(itemRecipes[i]))])+" in "+machineNames[itemMachines[i]])+value*(", value: "+str(itemPrices[i]))+cost*(", cost: "+str(sumResourceCosts[i]))+specific*(", specific: "+str(specificResourceCosts[i]))+starterUpperBound*(","+" "*(max(len(i) for i in itemNames)-len(itemNames[i]))+" starter upper bound: "+unitToDisplay))

for i in range(len(itemRecipes)):
    fractionsMode=(itemFractions[i][1]>1)
    if fractionsMode:
        unitToDisplay=str(itemFractions[i][0])+"/"+str(itemFractions[i][1])
    else:
        unitToDisplay=int(itemStarterUpperBounds[i][1])
        if itemStarterUpperBounds[i][1]<1:
            unitToDisplay=1/unitToDisplay
        unitToDisplay=str(unitToDisplay)
    unitToDisplay+=(" seconds/"+itemNames[i] if itemStarterUpperBounds[i][1]<1 and not fractionsMode else " "+itemPlurals[i]+"/second")
    itemReport(i,0,0,0,0,1)
    #print(" "*(indentation+2)+str(itemProcessingCosts[i]))
    print(" "*(indentation+2+max(len(i) for i in itemNames)+4)+"space upper bound: "+str(itemSpaceUpperBounds[i])+" "+itemPlurals[i]+"/second")
