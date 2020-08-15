import pygame
import random
import tkinter as tk
pygame.init()


# define colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (200, 200, 0)
bright_yellow = (255, 255, 0)
future_blue = (92, 149, 192)

grid = []
checked = []
stack = []
solution = {}

#gridX = 20
#gridY = 20
x = 0
y = 0
window = tk.Tk()
window.title("Maze Generator and Solver")
window.geometry("600x600")
canvas = tk.Canvas(window,width = 600, height = 600,borderwidth=0, highlightthickness=0, bg="red")
close = False

def Close():
    global gridX,gridY,speed
    gridX = InpX.get()
    gridY = InpY.get()
    speed = speed_get.get()
    window.destroy()

def Quit():
    global close
    close = True
    window.destroy()
tk.Label(text="Enter the number of horizontal squares you want in the maze:",bg = "red").place(x=30,y=120)
tk.Label(text="Enter the number of vertical squares you want in the maze:",bg = "red").place(x=30,y=150)

InpX = tk.IntVar()
XE = tk.Entry(window,textvariable = InpX)
XE.place(x=380,y=120)
XE.insert(0,2)

InpY = tk.IntVar()
YE = tk.Entry(window,textvariable = InpY)
YE.place(x=380,y=150)
YE.insert(0,2)

speed_get = tk.IntVar()
sp1 = tk.Radiobutton(window,text="Fast",variable=speed_get,value=1)
sp1.pack(anchor = "s")
sp1.deselect()
sp2 = tk.Radiobutton(window,text="Slow",variable=speed_get,value=2)
sp2.pack(anchor = "s")
sp2.select()

tk.Button(window,text ="Start", width="7", bg="white", command=Close).place(x=300,y=200)
window.protocol( "WM_DELETE_WINDOW", Quit )
canvas.pack()
window.mainloop()
if not close:
    if gridY <= 30 and gridX <= 30:
        block_size = 25
    elif gridY <= 50:
        block_size = 15
    elif gridY <= 75:
        block_size = 10
    elif gridY <= 100 or gridX <=100:
        block_size = 7
    elif gridY <= 150 or gridX<=150:
        block_size = 5
    elif gridY <= 200 or gridX<=200:
        block_size = 4
    else:
        block_size = 2
    width = (gridX * block_size) + block_size + gridX #- int(gridX/2)
    height = (gridY * block_size) + block_size + gridY
    win = pygame.display.set_mode((width, height))
    win.fill(black)
    pygame.display.set_caption("Maze Generator and Solver")

    def draw_grid(x, y,gridX,gridY):
        for i in range(gridY):
            x = gridX
            y += block_size
            for j in range(gridX):
                pygame.draw.line(win, green, [x, y], [x + block_size, y])  # top of cell
                pygame.draw.line(win, green, [x + block_size, y], [x + block_size, y + block_size])  # right of cell
                pygame.draw.line(win, green, [x + block_size, y + block_size], [x, y + block_size])  # bottom of cell
                pygame.draw.line(win, green, [x, y + block_size], [x, y])
                grid.append((x, y))
                x += block_size


    def push_up(x, y):
        pygame.draw.rect(win, white, (x + 1, y - block_size + 1, block_size-1, (block_size*2) - 1), 0)  # draw a rectangle twice the width of the cell
        pygame.display.update()  # to animate the wall being removed


    def push_down(x, y):
        pygame.draw.rect(win, white, (x + 1, y + 1, block_size-1, (block_size*2)-1), 0)
        pygame.display.update()


    def push_left(x, y):
        pygame.draw.rect(win, white, (x - block_size + 1, y + 1, (block_size*2)-1, block_size-1), 0)
        pygame.display.update()


    def push_right(x, y):
        pygame.draw.rect(win, white, (x + 1, y + 1, (block_size*2)-1, block_size-1), 0)
        pygame.display.update()


    def back_cell(x, y):
        pygame.draw.rect(win, green, (x + 1, y + 1, block_size-2, block_size-2), 0)  # draw a single width cell
        pygame.display.update()


    def color_cell(x, y):
        pygame.draw.rect(win, white, (x + 1, y + 1, block_size-2, block_size-2), 0)  # recolor the path
        pygame.display.update()


    def solution_cell(x, y):
        pygame.draw.rect(win, yellow, (((x + x + block_size)/2)-2, ((y + y + block_size)/2)-2, 5, 5), 0)  # solution
        pygame.display.update()


    def randomize(x, y):
        global cont
        back_cell(x, y)
        stack.append((x, y))
        checked.append((x, y))
        while len(stack) > 0 and cont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cont = False
                    pygame.quit()
            if speed == 2:
                pygame.time.delay(100)
            cell = []
            if (x + block_size, y) not in checked and (x + block_size, y) in grid:
                cell.append("right")
            if (x - block_size, y) not in checked and (x - block_size, y) in grid:
                cell.append("left")
            if (x, y + block_size) not in checked and (x, y + block_size) in grid:
                cell.append("down")
            if (x, y - block_size) not in checked and (x, y - block_size) in grid:
                cell.append("up")

            if len(cell) > 0:
                rand_cell = random.choice(cell)
                if rand_cell == "right":
                    push_right(x, y)
                    solution[(x + block_size, y)] = x, y
                    x = x + block_size
                    checked.append((x, y))
                    stack.append((x, y))
                elif rand_cell == "left":
                    push_left(x, y)
                    solution[(x - block_size, y)] = x, y
                    x = x - block_size
                    checked.append((x, y))
                    stack.append((x, y))
                elif rand_cell == "up":
                    push_up(x, y)
                    solution[(x, y - block_size)] = x, y
                    y = y - block_size
                    checked.append((x, y))
                    stack.append((x, y))
                elif rand_cell == "down":
                    push_down(x, y)
                    solution[(x, y + block_size)] = x, y
                    y = y + block_size
                    checked.append((x, y))
                    stack.append((x, y))
            else:
                x, y = stack.pop()
                back_cell(x, y) #go back a cell to show that it's being removed
                if speed == 2:
                    pygame.time.delay(50)
                color_cell(x, y)


    def back_track():
        #recursive backtracking
        select = False
        Quit = False
        while not select:
            font = pygame.font.SysFont("comicsans",22)
            text = font.render("Choose an end point",0,red)
            win.blit(text,(gridX + 45,2))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    select = True
            #print(mouse)
            for i in grid:
                if i[0] + block_size > mouse[0] > i[0] and i[1] + block_size > mouse[1] > i[1]:
                    pygame.draw.rect(win,red,(i[0]+1,i[1]+1,block_size-2,block_size-2))
                    if click[0] == 1:
                        x = i[0]
                        y = i[1]
                        pygame.draw.rect(win, white, (i[0] + 1, i[1] + 1, block_size-2, block_size-2))
                        select = True
                        break

                else:
                    pygame.draw.rect(win, white, (i[0] + 1, i[1] + 1, block_size-2, block_size-2))
            pygame.display.update()
        solution_cell(x, y)  # list containing all the coordinates to route back to the start
        while (x, y) != (gridX, 0) and not Quit:  # loop until current cell position == start position
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Quit = True
                    pygame.quit()
            x,y = solution[x,y]    #change the key value to the new value
            solution_cell(x, y)  # draw the route back
            if speed == 2:
                pygame.time.delay(100)

    x, y = gridX, 0
    run = True
    cont = True
    draw_grid(x, y,gridX,gridY)
    if cont:
        randomize(x, y)
    if cont:
        back_track()

    clock = pygame.time.Clock()

    while run:
        pygame.event.get()
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break
