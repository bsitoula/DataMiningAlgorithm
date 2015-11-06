__author__ = 'bibassitoula'
import itertools
import time

def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def getItemSetValue(itemset,itemsetCollection):
    count = 0
    for everyItemSet in itemsetCollection:
        length = len(itemset)
        orgLen = len(itemset)
        index = 0
        length2 = 0
        while length > 0:
            if everyItemSet.count(itemset[index]) >= 1:
                length2 = length2 + 1
            length = length -1
            index = index + 1
        if length2 == orgLen:
            count = count + 1
    return count

def itemSetGenerator(previousItemset,width,refinedItemSet,minsupcount,newdataSet):
    comparingLength = width - 2
    #print(comparingLength)
    d = []
    temp = []
    for i in range(0,len(previousItemset)-1):
        firstSet = previousItemset[i]
        if(refinedItemSet[firstSet] >= minsupcount):
            for j in range(i+1, len(previousItemset)):
                secondSet = previousItemset[j]
                flag = 0
                if(refinedItemSet[secondSet] >= minsupcount):
                    for k in range(0,comparingLength):
                        if firstSet[k] == secondSet[k]:
                            flag = flag + 1
                    if flag == comparingLength:
                        for m in range(0,width-1):
                            temp.append(firstSet[m])
                        temp.append(secondSet[-1])
                        newSet = tuple(temp)
                        value = getItemSetValue(newSet,newdataSet)
                        if value >= minsupcount:
                            d.append(newSet)
                            refinedItemSet[newSet] = value
                        temp = []
    return d

def associationRules(refinedItemSet,minconf,minsup,array_2,uniqueitemSetValue):
    print("association rules ========= confidence ========== Support")
    for key, value in refinedItemSet.items():
        if type(key) != int:
            if len(key) == 2:
                support = float(getItemSetValue(key,array_2))/len(array_2)
                confidence = float(getItemSetValue(key,array_2))/uniqueitemSetValue[key[0]]
                if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                    print(str(key[0])+" ===> "+str(key[1])+" ===== "+str(confidence)+" === "+str(support))
                support = ''
                confidence = ''
                support = float(getItemSetValue(key,array_2))/len(array_2)
                confidence = float(getItemSetValue(key,array_2))/uniqueitemSetValue[key[1]]
                if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                    print(str(key[1])+" ===> "+str(key[0])+" ===== "+str(confidence)+" === "+str(support))
                support = ''
                confidence = ''

            if len(key) > 2:
                iteration = len(key)/2
                for i in range(0,iteration):
                    b = sorted(findsubsets(key,2))
                    for everytuple in b:
                        missing = tuple(set(list(key))-set(list(everytuple)))
                        if len(missing) == 1:
                            support = float(getItemSetValue(key,array_2))/len(array_2)
                            confidence = float(getItemSetValue(key,array_2))/getItemSetValue(everytuple,array_2)
                            if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                                print(str(everytuple)+" ===> "+str(missing[0])+" ===== "+str(confidence)+" === "+str(support))
                            support = ''
                            confidence = ''
                            support = float(getItemSetValue(key,array_2))/len(array_2)
                            confidence = float(getItemSetValue(key,array_2))/uniqueitemSetValue[missing[0]]
                            if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                                print(str(missing[0])+" ===> "+str(everytuple)+" ===== "+str(confidence)+" === "+str(support))
                            support = ''
                            confidence = ''
                        else:
                            support = float(getItemSetValue(key,array_2))/len(array_2)
                            confidence = float(getItemSetValue(key,array_2))/getItemSetValue(everytuple,array_2)
                            if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                                print(str(everytuple)+" ===> "+str(missing)+" ===== "+str(confidence)+" === "+str(support))
                            support = ''
                            confidence = ''
                            support = float(getItemSetValue(key,array_2))/len(array_2)
                            confidence = float(getItemSetValue(key,array_2))/getItemSetValue(missing,array_2)
                            if (support*len(array_2)) >= minsup and (confidence*len(array_2)) >=minconf:
                                print(str(missing)+" ===> "+str(everytuple)+" ===== "+str(confidence)+" === "+str(support))
                            support = ''
                            confidence = ''

def apriori(dataset,minisup,minconf):
    minsup = (minisup * len(dataset))/100
    minconf = (minconf * len(dataset))/100
    originalItemset = dataset
    uniqueItemsValues = {}
    refinedItemSet = {}
    unrefinedItemset = {}
    itemset = []
    c = []
    for everyItemSet in originalItemset:

        everyItemSet = everyItemSet
        for everyItem in everyItemSet:
            everyItem = int(everyItem)
            if everyItem not in uniqueItemsValues:
                uniqueItemsValues[everyItem] = 0
            if everyItem in uniqueItemsValues:
                uniqueItemsValues[everyItem] = uniqueItemsValues[everyItem] + 1

    for key, value in uniqueItemsValues.items():
        unrefinedItemset[key] = value
        if value >= minsup:
            refinedItemSet[key] = value
            itemset.append(key)

    itemset = sorted(itemset)

    for i in range(0,len(itemset)-1):
        for j in range(i+1,len(itemset)):
            #print(j)
            key = itemset[i],itemset[j]
            value = getItemSetValue(key,dataset)
            unrefinedItemset[key] = value
            if value >= minsup:
                refinedItemSet[key] = value
                c.append(key)

    width = 3
    while width > 0:
        newItemSet = itemSetGenerator(c,width,refinedItemSet,minsup,dataset)

        if(not newItemSet):
            break
        c = []
        c = newItemSet
        newItemSet = []
        width = width + 1

    print("FREQUENT ITEMSET =====>  COUNT")
    printed = 0
    count = 0
    while printed < len(refinedItemSet):
        for key,value in refinedItemSet.items():
            if type(key) == int and count < 1:
                print(str(key) + "  ========>  " + str(value))
                printed = printed+1

            elif type(key) != int:
                if len(key) == count:
                    print(str(key) + "  ========>  " + str(value))
                    printed = printed + 1
        count = count+1
    return refinedItemSet,uniqueItemsValues

if __name__ == '__main__':
    print("###############  Loading the Transactions    ######################")

    ## Provide the Link to the data file here
    filePath = ""
    with open(filePath, "r") as ins:
        array = []
        items = []
        array2 = []
        ln = 0
        for line in ins:
            ln=ln+1
            for item in line.split():
                items.append(int(item))
            array.append(line)
            array2.append(items)
            items = []
    print("###############   "+ str(len(array2)) + "   Transactions Loaded Completely ################")
    print("######## FREQUENT ITEMSET GENERATION USING THE APRIORI ALGORITHM #####################")

    ##### CHANGE THE VALUE OF MINIMUM SUPPORT AND CONFIDENCE HERE FOR APRIORI
    MINUMUM_SUPPORT_THRESHOLD = 20
    MINIMUM_CONFIDENCE_THRESHOLD = 5
    START_TIME = time.time()
    aprioriItemSet = apriori(array2,MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD)
    END_TIME = time.time()
    print("APRIORI EXECUTION TIME "+str(END_TIME-START_TIME))
    print("######################################## END OF APRIORI ALGORITHM ##########################################")

    print("############## ASSOCIATION RULE GENERATION FOR THE FREQUENT ITEMSET GENERATED ##############################")
    print(len(aprioriItemSet[0]))
    associationRules(aprioriItemSet[0],MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD,array2,aprioriItemSet[1])
    print("#############################")
    print("#############################")
    print("#############################")
    print("######## FREQUENT ITEMSET GENERATION USING THE SIMPLE RANDOM ALGORITHM #####################")

    ############ CHANGE THE SAMPLE SIZE HERE FOR SIMPLE RANDOM ALGORITHM
    SAMPLE_OF_SIZES = 50
    subsetLength = (len(array2)*SAMPLE_OF_SIZES)/100
    simpleRandomDataset = []
    dataset = {}
    for i in range(0,subsetLength):
        simpleRandomDataset.append(array2[i])
    START_TIME = time.time()
    dataset = apriori(simpleRandomDataset,MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD)
    END_TIME = time.time()
    print("SIMPLE RANDOM EXECUTION TIME " + str(END_TIME-START_TIME))
    print("################################# END OF SIMPLE RANDOM ALGORITHM ##########################################")
    print("############## ASSOCIATION RULE GENERATION FOR THE FREQUENT ITEMSET GENERATED ##############################")
    associationRules(dataset[0],MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD,simpleRandomDataset,dataset[1])
    print("#############################")
    print("#############################")
    print("#############################")
    print("################ FREQUENT ITEMSET GENERATION USING THE SON ALGORITHM ###########################")

    ############# CHANGE THE NUMBER OF PARTITION HERE FOR SON ALGORITHM
    PARTITION = 3
    print("THE NUMBER OF PARTITION USED IS "+ str(PARTITION))
    LIST_SON = []
    k = 0
    l = 0
    SON_DATA = {}
    DATA = {}
    TOTAL_TIME = []
    PARTITION_LENGTH = len(array2) / PARTITION
    for i in range(0,PARTITION):
        k = l
        l = l + PARTITION_LENGTH
        if i+1 == PARTITION:
            DATA[i] = array2[k:l+1]
        else:
            DATA[i] = array2[k:l]
    for key,value in DATA.items():
        a = ''
        START_TIME = time.time()
        a = apriori(value,MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD)
        END_TIME = time.time()
        TOTAL_TIME.append(END_TIME-START_TIME)
        for key1,val1 in a[0].items():
            if key1 in SON_DATA:
                SON_DATA[key1] = SON_DATA[key1] + val1
            else:
                SON_DATA[key1] = val1
    print("SON EXECUTION TIME " + str(sum(TOTAL_TIME)))
    print("## AFTER COMBINING ALL THE PARTITION THE SUM OF THE SIMILAR ITEMSET FROM DIFFERENT PARTITION IS #########")
    print(SON_DATA)
    print("###################################### END OF SON ALGORITHM ################################################")
    print("############## ASSOCIATION RULE GENERATION FOR THE FREQUENT ITEMSET GENERATED ##############################")
    associationRules(SON_DATA,MINUMUM_SUPPORT_THRESHOLD,MINIMUM_CONFIDENCE_THRESHOLD,array2,aprioriItemSet[1])


