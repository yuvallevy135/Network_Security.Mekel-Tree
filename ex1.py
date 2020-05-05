from hashlib import sha256
import math

class Node:
    def __init__(self, data, l_son, r_son, minimum, maximum):
        self.data = data  # Assign data
        self.father = None  # Initialize next as null
        self.left_son = l_son
        self.right_son = r_son
        self.min = minimum
        self.max = maximum


def createNode(str, l_son, r_son, min_index, max_index):
    node = Node(str, l_son, r_son, min_index, max_index)
    return node


def createLeafNodes(inputList):
    leafArray = []
    for i in range(1, len(inputList)):
        leafArray.append(createNode(inputList[i], None, None, i - 1, i - 1))
    return leafArray


def buildMerkleTree(leafList):
    if len(leafList) is 1:
        return leafList[0]
    father_List = []
    for i in range(0, len(leafList), 2):
        mixedString = str(leafList[i].data + leafList[i+1].data)
        hashedString = sha256(mixedString.encode())
        father_node = createNode(hashedString.hexdigest(),
                                 leafList[i], leafList[i + 1], leafList[i].min, leafList[i + 1].max)
        leafList[i].father = father_node
        leafList[i + 1].father = father_node
        father_List.append(father_node)
    root = buildMerkleTree(father_List)
    return root


def proofOfInclusion(r, treeDepth, requiredIndex):
    retString = ""
    proofList = []
    currNode = r
    for i in range(0, treeDepth + 1):
        if currNode.min == requiredIndex and currNode.max == requiredIndex:
            for j in range(len(proofList) - 1, -1, -1):
                retString = retString + proofList[j][0] + " "
                retString = retString + proofList[j][1].data + " "
            retString = retString[:-1]
            print(retString)

            return
        if i == treeDepth:
            exit(1)
        if requiredIndex < currNode.right_son.min:
            proofList.append(('r', currNode.right_son))
            currNode = currNode.left_son
        else:
            proofList.append(('l', currNode.left_son))
            currNode = currNode.right_son


root = None
depth = 0
leafList = []
while True:
    msg = input()
    inputList = msg.split(' ')
    command = inputList[0]

    if command is '1':
        depth = int(math.log2(len(inputList)))
        leafList = createLeafNodes(inputList)
        root = buildMerkleTree(leafList)
        print(root.data)
    elif command is '2':
        if len(inputList) != 2 or root is None or not(inputList[1].isdigit()):
            exit(1)
        requiredLeafIndex = int(inputList[1])
        if requiredLeafIndex >= len(leafList) or requiredLeafIndex < 0:
            exit(1)
        proofOfInclusion(root, depth, requiredLeafIndex)
    elif command is '3':
        if len(inputList) < 5 or len(inputList) % 2 == 0:
            exit(1)
        proof = []
        mixedString = ""
        parentHash = ""
        requiredLeaf = inputList[1]
        rootHash = inputList[2]
        # create a proof of inclusion pair list
        for i in range(3, len(inputList), 2):
            proof.append((inputList[i], inputList[i + 1]))
        if proof[0][0] == 'l':
            mixedString = str(proof[0][1] + requiredLeaf)
        elif proof[0][0] == 'r':
            mixedString = str(requiredLeaf + proof[0][1])
        else:
            exit(1)
        parentHash = sha256(mixedString.encode()).hexdigest()
        for j in range(1, len(proof)):
            if proof[j][0] == 'l':
                mixedString = str(proof[j][1] + parentHash)
            elif proof[j][0] == 'r':
                mixedString = str(parentHash + proof[j][1])
            else:
                exit(1)
            parentHash = sha256(mixedString.encode()).hexdigest()
        if parentHash == rootHash:
            print(True)
        else:
            print(False)
    elif command is '4':
        if len(inputList) != 2 or root is None or not(inputList[1].isdigit()):
            exit(1)
        # if root is None:
        #     exit(1)
        numOfZeros = int(inputList[1])
        zeroString = ""
        for j in range(0, numOfZeros):
            zeroString = zeroString + '0'
        i = 0
        hashedString = ""
        while True:
            mixedString = str(str(i) + root.data)
            hashedString = sha256(mixedString.encode()).hexdigest()
            if hashedString[:numOfZeros] == zeroString:
                print(i, end=' ')
                print(hashedString)
                break
            i = i + 1
    elif command is '5':
        break
    else:
        break
exit(1)
