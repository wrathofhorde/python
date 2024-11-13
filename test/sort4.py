def selection_sort(array, comp):
  for start_idx in range(len(array) - 1):
    selected_idx = start_idx
    
    for idx in range(start_idx + 1, len(array)):
      if comp(array[selected_idx], array[idx]):
          selected_idx = idx

    temp = array[start_idx]
    array[start_idx] = array[selected_idx]
    array[selected_idx] = temp

if __name__ == "__main__":
  def ascend(lhs, rhs):
    return True if lhs > rhs else False

  def descend(lhs, rhs):
    return True if lhs < rhs else False
  
  scores = [5, 2, 9, 3, 4] # 무작위
  selection_sort(scores, ascend)
  print(scores)
  selection_sort(scores, descend)
  print(scores)

