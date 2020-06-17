list1 = ''
list2 = ''
list3 = ''
result = ''

for i in range(5, 0, -1):
    if len(list2) < 2:
        
        list1 = (i * 'O')
        list2 = ((5-i) * 'O')
        
    else:
        
        list1 = ((i + 1) * 'O')
        list2 = ((len(list2) - 1) * 'O')
        list3 = list2
    if list1 > list2:
        result = list1
        if len(list2) > 0 and len(list3) > 0:
            result += '\n' + list2 + '\n' + list3
        elif len(list2) > 0:
            result += '\n' + list2
    
            
        print(result)
        print('----------')