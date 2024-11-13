def ascend(lhs, rhs):
  return True if lhs > rhs else False

def descend(lhs, rhs):
  return True if lhs < rhs else False
  
def selection_sort(array, ascending):
  comp = ascend if ascending == True else descend

  for start_idx in range(len(array) - 1): # 마지막 요소의 앞(n - 1)까지만 비교 
    selected_idx = start_idx # 시작하는 요소에 최소값이 있다고 가정
    
    for idx in range(start_idx + 1, len(array)):
      if comp(array[selected_idx], array[idx]):
          selected_idx = idx

    temp = array[start_idx]
    array[start_idx] = array[selected_idx]
    array[selected_idx] = temp

if __name__ == "__main__":
  scores = [5, 2, 9, 3, 4] # 무작위
  selection_sort(scores, True)
  print(scores)
  selection_sort(scores, False)
  print(scores)

