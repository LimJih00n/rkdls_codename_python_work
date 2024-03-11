class GameObject:
    _id_counter = 0
    
    def __init__(self, x, y, w, h, hit_x, hit_y, hit_w, hit_h, direction, dx, dy, state, img_dic):
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        self._direction = direction
        self._dx = dx
        self._dy = dy
        self._state = state
        self._img_dic = img_dic
        self._hit_x = hit_x
        self._hit_y = hit_y
        self._hit_w = hit_w
        self._hit_h = hit_h
        self._id = GameObject._id_counter  # 객체별 유니크 ID 할당
        GameObject._id_counter += 1

    # Getter methods
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_direction(self):
        return self._direction

    def get_dx(self):
        return self._dx

    def get_dy(self):
        return self._dy

    def get_state(self):
        return self._state

    def get_img_dic(self):
        return self._img_dic

    def get_hit_x(self):
        return self._hit_x

    def get_hit_y(self):
        return self._hit_y

    def get_hit_w(self):
        return self._hit_w

    def get_hit_h(self):
        return self._hit_h

    def get_id(self):
        return self._id

    #init정리필요!
    def update_position(self):
        if self._direction == 'U':
            self._hit_y -= self._dy
            self._y -= self._dy
        elif self._direction == 'D':
            self._hit_y += self._dy
            self._y += self._dy
        elif self._direction == 'R':
            self._hit_x += self._dx
            self._x += self._dx
        elif self._direction == 'L':
            self._hit_x -= self._dx
            self._x -= self._dx
        elif self._direction == 'S':
            pass  # 정지 상태
    
    def set_direction(self,dir):
        self._direction = dir
        
    def set_velocity(self,dx,dy):
        self._dx = dx
        self._dy = dy
    
    def set_state(self,state):
        self._state = state
    
    def turn_left(self):
        direction_order = ['U', 'L', 'D', 'R']
        current_index = direction_order.index(self._direction)
        self._direction = direction_order[(current_index + 1) % 4]

    def turn_right(self):
        direction_order = ['U', 'R', 'D', 'L']
        current_index = direction_order.index(self._direction)
        self._direction = direction_order[(current_index + 1) % 4]
        
   
    def check_collision(self, other):
    # A의 오른쪽 경계가 B의 왼쪽 경계보다 오른쪽에 있는지 확인
        right_of_other_left = self._hit_w + self._hit_x >  other.get_hit_x()
        # A의 왼쪽 경계가 B의 오른쪽 경계보다 왼쪽에 있는지 확인
        left_of_other_right = self._hit_x <  other.get_hit_w() + other.get_hit_x()
        # A의 하단 경계가 B의 상단 경계보다 아래에 있는지 확인
        below_other_top = self._hit_h + self._hit_y > other.get_hit_y()
        # A의 상단 경계가 B의 하단 경계보다 위에 있는지 확인
        above_other_bottom =  self._hit_y <  other.get_hit_h() + other.get_hit_y()
        

        # 모든 조건이 참이면 충돌 발생
        if right_of_other_left and left_of_other_right and below_other_top and above_other_bottom:
            return True
        else:
            return False

        

class Hero(GameObject):
    def __init__(self, x, y, w, h,hit_x,hit_y,hit_w,hit_h, direction='S', dx=0, dy=0,state="default",img_dic={}):
        super().__init__(x, y, w, h,hit_x,hit_y,hit_w,hit_h,direction, dx, dy,state,img_dic)

class Wall(GameObject):
    def __init__(self, x, y, w, h,hit_x,hit_y,hit_w,hit_h, direction='S', dx=0, dy=0,state="default",img_dic={}):
        super().__init__(x, y, w, h,hit_x,hit_y,hit_w,hit_h,direction, dx, dy,state,img_dic)
    
    def move_left_right(self,X):
        if self._x > X-self._width and self._state == "right":
            self._direction = "L"
            self._state = "left"
        elif self._x<0 and self._state =="left":
            self._direction = "R"
            self._state ="right"
    
    def move_rectangle(self,X1,Y1,X2,Y2):
        
        if self._x < X1 and self._y < Y1 and self._direction == "U":
            self._direction = "R"
            self._state = "right"
        elif self._x > X2 and self._direction == "R":
            self._direction = "D"
            self._state = "left"
        elif self._x > X2 and self._y>Y2 and self._direction == "D":
            self._direction = "L"
            self._state = "left"
        elif self._x<X1 and self._direction == "L":
            self._direction = "U"
            self._state = "right"
        
        
            
        

class Background(GameObject):
    def __init__(self, x, y, w, h,hit_x,hit_y,hit_w,hit_h, direction='S', dx=0, dy=0,state="default",img_dic={}):
        super().__init__(x, y, w, h,hit_x,hit_y,hit_w,hit_h,direction, dx, dy,state,img_dic)



class Item(GameObject):
    def __init__(self, x, y, w, h,hit_x,hit_y,hit_w,hit_h, direction='S', dx=0, dy=0,state="default",img_dic={}):
        super().__init__(x, y, w, h,hit_x,hit_y,hit_w,hit_h,direction, dx, dy,state,img_dic)
        
class Monster(GameObject):
    def __init__(self, x, y, w, h,hit_x,hit_y,hit_w,hit_h, direction='S', dx=0, dy=0,state="default",img_dic={}):
        super().__init__(x, y, w, h,hit_x,hit_y,hit_w,hit_h,direction, dx, dy,state,img_dic)


