def selection_sort(array):
  for start_idx in range(len(array) - 1): # 마지막 요소의 앞(n - 1)까지만 비교 
    selected_idx = start_idx # 시작하는 요소에 최소값이 있다고 가정
    
    for idx in range(start_idx + 1, len(array)): # start 다음 요소부터 마지막까지 비교
      if array[selected_idx] > array[idx]: # 선택된 요소값보가 작은 값이 나타나면
        selected_idx = idx # 새로운 인덱스를 선택

    # 저장된 값을 교환
    temp = array[start_idx]
    array[start_idx] = array[selected_idx]
    array[selected_idx] = temp
    # array[start_idx], array[selected_idx] = array[selected_idx], array[start_idx]

if __name__ == "__main__":
  scores = [5, 2, 9, 3, 4] # 무작위
  selection_sort(scores)
  print(scores)

  scores = [1, 2, 3, 4, 5] # 정렬된 값
  selection_sort(scores)
  print(scores)

  scores = [5, 4, 3, 2, 1] # 역순
  selection_sort(scores)
  print(scores)
