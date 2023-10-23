'''
Wind is the shifter for numbers.
'''

ground = [[0, 0, 0, 0], 
          [0, 2, 3, 3], 
          [0, 1, 2, 0], 
          [0, 0, 0, 1]]


d = h = w = 4
wind = str('r').upper()
start = 0
stop= 0
step = 0

if wind == 'L' or wind == 'T':
    start = d - 1
    stop = 0
    step = -1
if wind == 'R' or wind == 'B':
    stop = d - 1


print('---------from original----------')
for plot in ground:    
    print(plot)


if wind == 'L':
    '''blowing from left'''
    for plot in ground:    
        for id in range(start, stop , step):
            plot[id] = plot[id-1]
    print('---------from left----------')
    for plot in ground:    
        print(plot)


if wind == 'R':
    '''blowing from right'''
    for plot in ground:    
        for id in range(stop):
            plot[id] = plot[id+1]
        plot[d-1] = 0
    print('--------from right-----------')
    for plot in ground:    
        print(plot)


if wind == 'T':
    '''blowing from top'''
    for id in range(start, stop, step):
        ground[id] = ground[id-1]
    print('--------from top-----------')
    for plot in ground:    
        print(plot)


if wind == 'B':
    '''blowing from botton'''
    for id in range(stop):
        ground[id] = ground[id+1]
    ground[h-1] = [0]*4
    print('--------from botton-----------')
    for plot in ground:    
        print(plot)
