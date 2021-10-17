import heapq

def mid_num(arr):
    l = len(arr)//2+1
    hp = [-x for x in arr[:l]]
    heapq.heapify(hp)
    for k in range(l,len(arr)):
        if -hp[0]>arr[k]:
            heapq.heappop(hp)
            heapq.heappush(hp,-arr[k])
    hp = [-x for x in hp]
    if len(arr)%2==0:
        return (hp[0]+hp[1])/2
    else:
        return hp[0]

if __name__ == '__main__':
    print(sorted([2,3,4,1,4,5,3,8]))
    print(mid_num([2,3,4,1,4,5,3,8]))