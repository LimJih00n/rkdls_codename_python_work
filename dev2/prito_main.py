import js
from js import document, window, Image, console
import world
import img_dic_set as ids
from pyodide import create_proxy
import datetime as dt
import asyncio

lastTime = 6
canvas = document.getElementById('Canvas')
canvas.width = 500
canvas.height = 500
ctx = canvas.getContext('2d')
console.log("Hey there, from 'console.log' inside PyScript!")
class DrawImage: # main에서만 js꺼 다룰 수 있음!
    def __init__(self,obj) -> None:
        self.image = Image.new()
        self.image.src = "!"
        self.x = obj.get_x()
        self.y = obj.get_y()
        self.height = obj.get_height()
        self.width = obj.get_width()
        self.state = "default"
        self.frame_idx = 0
        self.frame_length = 0
    
    
    def draw(self, obj):
        
        self.frame_length = obj.get_img_dic()[obj.get_state()]["frame"]
        frame_width_move = obj.get_img_dic()[obj.get_state()]["f-width-full"] // self.frame_length
        frame_width = obj.get_img_dic()[obj.get_state()]["f-width"]
        frame_height = obj.get_img_dic()[obj.get_state()]["f-height"]
        self.x = obj.get_x()
        self.y = obj.get_y()
        self.width = obj.get_width()
        self.height = obj.get_height()
        
        
        if self.image.src != "!" or self.state != obj.get_state():
            self.image.src = obj.get_img_dic()[obj.get_state()]["img-url"]
        self.state = obj.get_state()
                
        if obj.get_img_dic()[self.state]["frame"] == 1:
            ctx.drawImage(self.image, self.x, self.y, self.width, self.height)
        else:
            ctx.drawImage(
            self.image, 
            self.frame_idx *  frame_width_move, 0, # 스프라이트 시트에서의 x, y 위치
            frame_width, frame_height,    # 추출할 프레임의 너비와 높이
            self.x,self.y,                         # 캔버스 상의 x, y 위치
            self.width,self.height   # 캔버스 상의 프레임의 너비와 높이
            )
            self.frame_idx +=1
            self.frame_idx = (self.frame_idx + 1) % self.frame_length
        
        

# 방향애따라 그리는 것도 달라야함
# 이미지set있다면 그거 따라가기
def update_draw(obj_world,obj_js):
    obj_js.draw(obj_world)
    obj_world.update_position()
    
def check_out(obj):
    if obj.get_x() < 190 :
        return True
    if obj.get_x() + obj.get_width() > 260:
        return True
    if obj.get_y() < 90:
        return True
    if obj.get_y() + obj.get_height() > 360:
        return True
    return False

# 게임 완료 상태를 서버에 알리기

################################# user #########################
def UserInitCode():
    state = 0
#$user_init_start
    # Enter your code here
    warrior.set_direction("D")
    warrior.set_velocity(5,5)
#$user_init_out
def UserLoopCode():
    state=0
#$user_loop_start
    
#$user_loop_out
################################# user #########################


################################
# hit box!
# 움직ㅇ리때 hit box도 움직여야함 
# 실제 자기 box 다름!
# hit x,y: hit box의 시작좌표
# hit_w _h : hit box의 width와 height
################################


warrior = world.Hero(205,95,50,50,200,100,20,20,"S",0,0,"default",ids.knight_img_dic)

gold1 = world.Item(195,295,50,50,200,300,15,15,"S",0,0,"default",ids.gold_img_dic)
#gold2 = world.Item(200,200,50,50,225,200,50,50,"S",0,0,"default",ids.gold_img_dic)
#gold3 = world.Item(400,400,50,50,425,400,50,50,"S",0,0,"default",ids.gold_img_dic)

#sheep = world.Wall(0,225,65,65,0,250,65,50,"S",0,0,"right",ids.sheep_img_dic)
#goblin = world.Wall(350,350,60,60,360,350,50,60,"S",0,0,"right",ids.goblin_img_dic)
#tree1 = world.Wall(75,330,100,110,100,380,50,50,"S",0,0,"default",ids.tree_img_dic)
#tree2 = world.Wall(175,330,100,110,200,380,50,50,"S",0,0,"default",ids.tree_img_dic)
tree3 = world.Wall(225,180,100,110,250,200,50,50,"S",0,0,"default",ids.tree_img_dic)
castle = world.Wall(255,70,95,65,255,70,95,70,"S",0,0,"default",ids.Castle_img_dic)
house = world.Wall(300,75,45,65,300,75,45,65,"S",0,0,"default",ids.House_img_dic)
tower = world.Wall(295,345,50,95,300,345,50,50,"S",0,0,"default",ids.Tower_img_dic)



warrior_draw = DrawImage(warrior)
#goblin_draw = DrawImage(goblin)
castle_draw = DrawImage(castle)
#house_draw = DrawImage(house)
tower_draw = DrawImage(tower)
gold1_draw = DrawImage(gold1)
#gold2_draw = DrawImage(gold2)
#gold3_draw = DrawImage(gold3)
#tree1_draw = DrawImage(tree1)
#tree2_draw = DrawImage(tree2)
tree3_draw = DrawImage(tree3)
#sheep_draw = DrawImage(sheep)

background = world.Background(0,0,500,500,0,0,0,0,"S",0,0,"default",ids.background_img_dic)
background_draw = DrawImage(background)

# hitbox수정필요!
World_Walls = [tree3,tower,castle]
world_Items = [gold1]
World_objects_draw=[
                    (background,background_draw),
                    (warrior,warrior_draw),
                    #(sheep,sheep_draw),
                    #(goblin,goblin_draw),
                    #(tree1,tree1_draw),
                    #(tree2,tree2_draw),
                    (tree3,tree3_draw),
                    (castle,castle_draw),
                    #(house,house_draw),
                    (tower,tower_draw),
                    (gold1,gold1_draw),
                   
                    ]


Item_count = 0


#sheep.set_velocity(4,0)
#sheep.set_direction("R")
#sheep.move_left_right(500)

#goblin.set_velocity(4,4)
#goblin.set_direction("R")
#goblin.move_rectangle(340,340,440,440)

ratValue = 0
def frame_loop(*args):
    global lastTime
    global warrior_draw
    global warrior
    global castle
    global ratValue
    global Item_count
    global World_objects_draw
    
    #print(lastTime)
    
    
    if lastTime%5 ==0:
        
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        #sheep.move_left_right(500)
        #goblin.move_rectangle(340,340,440,440)
        #ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        # 그리는 부분 수정!
        for obj,draw in World_objects_draw:
            update_draw(obj,draw)
        
        
        for wall in World_Walls:
            if warrior.check_collision(wall):                                                                                                                    
                warrior.set_velocity(0,0)
        
        
        for item in world_Items:
            if warrior.check_collision(item):
                Item_count += 1
                world_Items.remove(item)
                #console.log(Item_count)
                World_objects_draw = [pair for pair in World_objects_draw if pair[0].get_id() != item.get_id()]
                #notify_server_game_completed()
                
                if Item_count == 1:
                    warrior.set_velocity(0,0)
                    notify_server_game_completed()
                
        if check_out(warrior):
            warrior.set_velocity(0,0)
        UserLoopCode()
        
    lastTime = lastTime+1 if lastTime <= float('inf') else 0    
    ratValue = window.requestAnimationFrame(create_proxy(frame_loop))
    
    
    #ctx.clearRect(0, 0, canvas.width, canvas.height)   
    #update_draw(rabbit,rabbit_draw)
    
    #window.requestAnimationFrame(create_proxy(frame_loop))


def controls(e):
    global warrior
    warrior.set_velocity(10,10)
    if e.code == 'KeyW':
        warrior.set_direction("U")
    elif e.code =='KeyS':
        warrior.set_direction("D")
    elif e.code == 'KeyA':
        warrior.set_direction("L")
        warrior.set_state("left")
    elif e.code == 'KeyD':
        warrior.set_direction("R")
        warrior.set_state("right")
        
document.addEventListener('keydown',create_proxy(controls))

frame_loop()
UserInitCode()




# => 시작함수 처음 시작할때만 작동합니다! => run으로 시작!
# => 반복함수 게임이 진행되는 동안 계속 작동합니다.
#=> 부분 나누기!