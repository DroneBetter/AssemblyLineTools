import math
raws=["copper","gold","iron","diamond","aluminium"] #and wriggling
processed=["liquid","gear","wire","plate"]
items=raws+[i+" "+j for j in processed for i in raws]
items+=["circuit","engine","heater plate","cooler plate","light bulb","clock","antenna","grill","toaster","air conditioner","battery","washing machine","solar panel","headphones","processor","drill","power supply","speakers","radio","jackhammer","TV","smartphone","fridge","tablet","microwave","railway","smartwatch","server rack","computer","generator","water heater","drone","electric board","oven","laser","advanced engine","electric generator","super computer","electric engine","AI processor","AI robot body","AI robot head","AI robot"]
machineNames=["starter","furnace","cutter","wire drawer","hydraulic press","crafter"]
itemMachines=[i for i in range(len(machineNames)) for j in range(len(raws))]
itemMachines+=[len(machineNames)-1]*(len(items)-len(itemMachines))
itemRecipes=[[]]*len(raws)+[[i] for i in range(len(raws))]*len(processed)+[[15,1],[12,11],[3,0,15],[3,1,16],[2,15],[2,1,10],[18,2],[27,2],[27,4,0],[28,1,4],[4,9,25],[26,4,0],[25,1,3],[25,16,18],[25,4],[3,10,26],[25,15,17],[25,16,18],[25,31,35],[25,3,22],[41,25,4],[39,35,4],[28,41,4],[39,35,4],[27,23,24],[2,22],[39,22,24],[24,4],[39,41,4],[26,20,21],[27,23,24],[35,39,24],[25,20,22],[27,20,22],[35,23,25],[26,25],[54,25,35],[53,52],[35,60],[62,25],[4,63,61],[64,4],[66,65]]
itemRecipeQuantities=[[1]]*len(raws)*(1+len(processed))+[[2,1],[2,1],[1,1,1],[1,1,1],[2,2],[2,2,1],[4,1],[1,4],[1,1,1],[1,1,1],[1,1,1],[1,2,2],[1,2,1],[1,1,1],[2,2],[2,2,1],[1,3,3],[2,4,4],[1,1,1],[4,4,4],[1,1,4],[1,1,2],[1,1,6],[1,1,4],[1,5,5],[10,10],[2,1,2],[20,10],[1,1,6],[4,5,5],[5,5,5],[2,2,4],[20,6,6],[10,10,10],[6,10,6],[50,50],[15,50,40],[30,10],[40,10],[4,40],[400,1,1],[1,200],[1,1]]
itemPrices=[80]*len(raws)+[100]*len(raws)*(len(processed)-1)+[250]*len(raws)+[300,360,360,360,360,540,540,600,900,900,1050,1100,1170,1300,1320,1500,1920,3300,5670,6920,7100,7300,7400,7600,8070,8400,10170,10600,11000,11820,12900,17220,27000,27300,31800,70000,470000,550000,900000,2500000,2800000,5000000,15000000]
itemResourceCosts=[]
itemSpaceCosts=[]
itemStarterUpperBounds=[]
specificResourceCosts=[]
itemFractions=[]
for i in range(len(itemRecipes)):
    if itemMachines[i]==0:
        itemResourceCosts.append(1)
        itemSpaceCosts.append(1/3)
        specificResourceCosts.append([int(k==i) for k in range(len(raws))])
    else:
        recipeSum=sum([itemRecipeQuantities[i][j] if itemMachines[itemRecipes[i][j]]==0 else math.ceil(itemRecipeQuantities[i][j]/3) for j in range(len(itemRecipes[i]))])
        itemResourceCosts.append(sum([itemRecipeQuantities[i][j]*itemResourceCosts[itemRecipes[i][j]] for j in range(len(itemRecipes[i]))]))
        itemSpaceCosts.append(1+(2/3 if itemMachines[i]!=5 else sum([itemRecipeQuantities[i][j]*itemSpaceCosts[itemRecipes[i][j]]+(itemMachines[itemRecipes[i][j]]==0)*(itemRecipeQuantities[i][j]%3)/3 for j in range(len(itemRecipes[i]))])+int(recipeSum>3)*math.ceil((recipeSum-3)/2))) #A single raw item in a recipe requires 1/3rd of a splitter and starter, two require 2/3rds of each (because three require two of each), three requires a splitter and no starters, so splitter cost is (raws%3)/3. In the upper bound case, if an item requires more than 3 ingredients, there are no optimisations where two items' excess rollers can be substituted for a single two-way splitter, because it would require having one input per output, while rollers need at least two to be worth having. If an item has raw materials in its recipe, it can use four inputs instead of three and output to the starter (to be picked up by a robot arm) but this requires 1/2 seconds output rate and uses an additional square regardless, so doesn't need to be considered in upper limits
        specificResourceCosts.append([sum([itemRecipeQuantities[i][j]*specificResourceCosts[itemRecipes[i][j]][k] for j in range(len(itemRecipes[i]))]) for k in range(len(raws))])
    multipleOfThree=0
    m=0
    while multipleOfThree==0:
        m+=1
        multipleOfThree=1
        for k in specificResourceCosts[i]:
            if (k*m)%3!=0:
                multipleOfThree=0
    upperBound=math.floor(56/(itemResourceCosts[i]*m/3))*3
    remainingStarters=56%(itemResourceCosts[i]*m/3)
    typesInItem=sum([int(k>0) for k in specificResourceCosts[i]])
    if typesInItem<=remainingStarters:
        remainingStarters-=typesInItem
        remainingCosts=[k-3*int(k>0) for k in specificResourceCosts[i]]
        bottleneckValue=1
        while remainingStarters>=0:
            bottleneckSet=0
            bottleneckIndex=0
            bottleneckValue=0
            for k in range(len(remainingCosts)):
                if specificResourceCosts[i][k]>0:
                    value=remainingCosts[k]/specificResourceCosts[i][k]
                    if bottleneckSet==0 or value>bottleneckValue or (value==bottleneckValue and specificResourceCosts[i][k]<specificResourceCosts[i][bottleneckIndex]):
                        bottleneckSet=1
                        bottleneckIndex=k
                        bottleneckValue=value
                        fraction=[specificResourceCosts[i][k]-remainingCosts[k],specificResourceCosts[i][k]]
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
    else:
        itemFractions.append([0,1])
    itemStarterUpperBounds.append([3*56/itemResourceCosts[i],upperBound])
    cellSecondsPerItem=0 #cells/(items/second)=cells*seconds/item

def itemReport(i,recipe,value,cost,specific,starterUpperBound):
    print(i, items[i]+recipe*(": "+str([str(itemRecipeQuantities[i][j])+" "+items[itemRecipes[i][j]] for j in range(len(itemRecipes[i]))])+" in "+machineNames[itemMachines[i]])+value*(", value: "+str(itemPrices[i]))+cost*(", cost: "+str(itemResourceCosts[i]))+specific*(", specific: "+str(specificResourceCosts[i]))+starterUpperBound*(", starter upper bound: "+unitToDisplay))

for i in range(len(itemRecipes)):
    itemFractions[i][0]+=math.floor(itemStarterUpperBounds[i][1])*itemFractions[i][1]
    fractionsMode=int(itemFractions[i][1]>1)
    if fractionsMode==1:
        unitToDisplay=str(itemFractions[i][0])+"/"+str(itemFractions[i][1])
    else:
        unitToDisplay=int(itemStarterUpperBounds[i][1])
        if itemStarterUpperBounds[i][1]<1:
            unitToDisplay=1/unitToDisplay
        unitToDisplay=str(unitToDisplay)
    if fractionsMode==0 and itemStarterUpperBounds[i][1]<1:
        unitToDisplay+=" seconds/"+items[i]
    else:
        unitToDisplay+=" "+items[i]+"s/second"
    itemReport(i,0,0,0,0,1)
    print(256/(itemSpaceCosts[i]+1/4))
