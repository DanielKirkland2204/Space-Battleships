import pygame
import random
import time
####COMMENCE THE PLACEMENT!#######
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.init()


"""DEFINE COLOURS"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LAVENDER = (172,124,250)
BLUE= (74,95,112)
MINT=(239,255,255)
GRAY=(211,211,211)
D_RED=(255,100,100)
"""initialise pygame sounds and display"""
display_width=875
display_height=600
sqr=30#Size of each square in the grid
# Set the width and height of the screen [width, height]
size = (display_width, display_height)
screen = pygame.display.set_mode(size) # change to the resolution

background = pygame.image.load('space_background.jpg').convert()
pygame.display.set_caption("Space Battleships")
screen.blit(background, [0, 0])


### Sounds files###
try:
    
    fire=pygame.mixer.Sound('laser.wav')
    strike=pygame.mixer.Sound('hit.wav')
    destroy=pygame.mixer.Sound('explosion.wav')
    #pygame.mixer.Sound.play(destroy)
# Loop until the user clicks the close button.
except:
    print ( "could not load or play soundfiles")
_sound_library=[fire,strike,destroy]
done = False

###Highlight types
EMP=10 #Empty place
HLD=11 #Highlighted
INV=12 #Invalid
HIT=20#Hit ship: this is added to the ship ID to define the ship's id while still alive.
MISS=14#Missed attack
DES=15#Destroyed ship
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

"""This class is used to play the sound and music files that the game uses. It is essential
that the sound files are in the same folder this code to avoid errors regarding missing files"""
class Sounds():
    def play_sound(s):
        global _sound_library
        file=_sound_library[s]
        sound=pygame.mixer.Sound(file)
        sound.set_volume(0.3)
        sound.play()
    def play_music(track):
        try:
            if track==1:
                trk='Space-Lament2.mp3'
            elif track==2:
                trk='Space-Lament-Defeat.mp3'
            elif track==3:
                trk='Space-Lament-Victory.mp3'
                
            music=pygame.mixer.music.load(trk)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except:
            print ("ERROR GETTING TRACKS")
"""PLAYER CLASS"""
"""This class focuses primarily on getting and setting the player's turn"""
class Player():
    def __init__(self,plyr):
        self.plyr=plyr
        
    def set_turn(self,plyr):
        try:
            if self.plyr==1:
                self.plyr=2
                 
            elif self.plyr==2:
                self.plyr=1

            elif self.plyr==0:
                self.plyr=1
        except ValueError:
            print ("Error Turn Value")
            self.player=0
        #print ("It is player: ",self.plyr, "'s turn.")
        return self.plyr
    
    def get_turn(self):
        return self.plyr

"""SHIP CLASS"""
"""The ship class is used to define each individual ship. """
class Ship(object):
    def __init__(self,ID,name,health):
        self.ID=ID
        self.name=name
        self.health=health


    def create_ship(ID,name,health):
        ship=Ship(ID,name,health)
        #print (ship)
        return ship
    
    def get_ship(ship,ID):
       #print(ship.name[ID])
        return ship.name[ID]
    
    def get_health(ship,ID):
        #print (ship.health[ID])
        return ship.health[ID]
    def set_health(self,ship,ID,Health):
        ship.health[ID]=Health
        #print ("Ship health set to ",ship.health[ID])


                
"""BOARD CLASS"""       
class Board(object):
    def __init__(self,row,col,width,height,margin,grid):#,width,height,margin,grid):
        self.col=col
        self.row=row
        self.width=width
        self.height=height
        self.margin=margin
        grid=(col,row)

    def create_board(self,width,height,margin,grid,plyr):
        #print ("Player is ",plyr)
        pos=520

       # print ("Updating board")
        for col in range(10):
            for row in range(10):
                #colour= WHITE
                if grid[row][col]==EMP or 5<=grid[row][col] <=9:#empty
                    colour=WHITE
                elif grid[row][col]==HLD:##highlighted
                    colour=BLUE
                elif 0<=grid[row][col] <=4:#ship
                    colour=LAVENDER
                #elif 5<=grid[row][col] <=9:#ship
                    #colour=LAVENDER
                elif grid[row][col]==INV:#invalid
                    colour=RED
                elif grid[row][col]>=HIT:
                    colour=GRAY
                elif grid[row][col]==MISS:
                    colour=BLACK
                elif grid[row][col]==DES:
                    colour=D_RED
                if plyr==1:    
                #               screen, colour,  width * number of squares, height of each square, w
                        pygame.draw.rect(screen, colour, [(width+margin) * row+margin,
                            (height+margin) * col +margin,
                            width,
                            height])
                elif plyr==2:
                        pygame.draw.rect(screen, colour, [(width+margin) * row+margin+pos,
                             (height+margin) * col
                                                          +margin,
                             width,
                             height])


    def display_boards(self,width,height,margin,grid,ogrid,plyr,oplyr):
        Board.create_board(self, width,height,margin,grid,plyr)
        Board.create_board(self, width,height,margin,ogrid,oplyr)
        Board.update_board()
    def reset_highlight(self,grid):
        try:
            for col in range(10):
                for row in range(10):
                    #print (grid[col][row])
                    if grid[col][row]==HLD or grid[col][row]==INV: 
                        grid[col][row]=EMP

        except ValueError:
            print ("Seems to have brought up a false alarm with co-ordinates")
    def Destroyed(self,grid,ID):
       # print("ID of Destroyed Vessel is ", ID)
        try:
            for col in range(10):
                for row in range(10):
                    if grid[col][row]==ID:# or grid[col][row]==INV:
                        
                        grid[col][row]=DES

        except ValueError:
            print ("Seems to have brought up a false alarm with co-ordinates")
        #pygame.display.flip()
    def set_ship(self,grid,ID):
        for col in range(10):
            for row in range(10):
                if grid[col][row]==HLD:
                    grid[col][row]=ID
                   # print ("After setting the ship, the value is ",grid[col][row])
                    
    def placement_check(self, placed,total):
        #print (placed)
        if placed != total:
            print ("still have ", total-placed, " ships to go.")
            return placed
        elif placed==total:
            return placed
    def update_board():
        pygame.display.flip()


class Attack_Pos(object):
    def __init__(self,row,col,direction,movement,pos):
        self.col=col
        self.row=row
        self.direction=direction
        self.movement=movement
        self.pos=(row,col)
    def set_direction(self,direction):
        self.direction=direction
    def get_direction(self):
        return self.direction
    def set_movement(self, movement):
        self.movement=movement
    def get_movement(self):
        return self.movement
    def set_pos(self,row,col):
        
        self.pos=(row,col)
        #print("SET POSITION!",self.pos)
    def get_pos(self):
        #print ("POSITION IS: ",self.pos)
        return self.pos
"""MESSAGE CLASS"""        
class Message():
    def text_objects(text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()
    def message_display(text,x,y):
        largeText = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = Message.text_objects(text, largeText)
        TextRect = ((x),(display_height/2+y))
        screen.blit(TextSurf, TextRect)

     
        #pygame.display.update()

    def reset_message():
        #print ("MSG 0")
        message=Message.message_display("1",100)
        message=Message.message_display("2",150)
        message=Message.message_display("3",200)
        message=Message.message_display("4",250)
        return (message)
    def attack_command(No,row,col,player,ship):
        screen.blit(background, [0, 0])
        message=""
        first=100#first line
        second=125#second line
        third=150#third line
        fourth=175#fourth line
        Column=str(col)
        Row=str(row)
        Ship=str(ship)
        x=0
        if player==1:
            x=450
            attacker="The enemy's "
        elif player==2:
            x=10
            attacker="Your "
        if No==1:

            #print ("MSG 7")

            message=Message.message_display("The attack missed at",x,first)
            message=Message.message_display("Co-ordinates: "+Row+", "+Column,x,second)
        elif No==2:
           # print ("MSG 8")
            message=Message.message_display(attacker+"ship was struck at "+Row+", "+Column,x,first)
        elif No==3:
            #print ("MSG 6")
            message=Message.message_display(attacker+Ship,x,second)
            message=Message.message_display(" has been destroyed.",x,third)
        

    def instructions(No,ship):
        screen.blit(background, [0, 0])
        message=""
        first=100#first line
        second=125#second line
        third=150#third line
        fourth=175#fourth line
        Ship=str(ship)
        shipType= str((Ship))
        x=10


        #print (shipType)
        if No==1:
            #print ("MSG 1")
            message=Message.message_display(Ship,x,first)
            message=Message.message_display("Place down the current ship by clicking on the grid.",x,second)
            message=Message.message_display("Press SPACE to change the direction your ship is facing.",x,third)
            message=Message.message_display("When you are happy with the position, press Enter.",x,fourth)
        elif No==2:
           # print ("MSG 2")
            message=Message.message_display(Ship,x,first)
            message=Message.message_display("Ship position is vertical.",x,second)
            message=Message.message_display("Press SPACE to change the direction your ship is facing.",x,third)
            message=Message.message_display("When you are happy with the position, press Enter.",x,fourth)
        elif No==3:
           # print ("MSG 3")
            message=Message.message_display(Ship,x,first)
            message=Message.message_display("Ship position is horizontal.",x,second)
            message=Message.message_display("Press SPACE to change the direction your ship is facing.",x,third)
            message=Message.message_display("When you are happy with the position, press Enter.",x,fourth)
        elif No==4:
           # print ("MSG 4")
            message=Message.message_display("You either haven't placed your ship or the position is invalid.",x,first)
            message=Message.message_display("Please Try Again.",x,second)


    def notifications(No):
        screen.blit(background, [0, 0])
        message=""
        first=100#first line
        second=125#second line
        third=150#third line
        fourth=175#fourth line
        x=325
        if No==1:
            #print ("MSG 5")
            message=Message.message_display("Incoming Enemy Fleet. . .",x,first)
        elif No==2:
           # print("Defeat")
            message=Message.message_display("Your fleet has been defeated. . .",x,first)
        elif No==3:
            #print("Victory")
            message=Message.message_display("Your fleet are VICTORIOUS!",x,first)


        #return message


"""GAME CLASS"""   
class Game():#Board,Ship,Player, Message):
    def __init__(self,width=sqr,height=sqr,margin=5,grid=[[EMP for x in range(10)] for y in range(10)],ogrid=[[EMP for x in range(10)] for y in range(10)],plyr=0):
        self.width=width
        self.height=height
        self.margin=margin
        self.grid=grid
        self.ogrid=ogrid
        self.plyr=plyr
        
        PID= [0,1,2,3,4,5,6,7,8,9]
        Name=["Assault Carrier","Battle Cruiser","Space Frigate","Heavy Fighter","Light Fighter","Assault Carrier","Battle Cruiser","Space Frigate","Heavy Fighter","Light Fighter"]
        #Names=[Name]
       # print ("Names: ",Name)
        Health=[5,4,3,3,2,5,4,3,3,2]
        #Health=[Ship_Health,Ship_Health]
        #OHealth=[5,4,3,3,2]
       # print("Before ",PShips)
        PShips=Ship.create_ship(PID,Name,Health)
        #OShips=Ship.create_ship(OID,Name,OHealth)
       # print (Ship.get_health(PShips,0))
       # print("Getting ships")
        Ship.get_health(PShips,0)
        Ship.get_ship(PShips,0)
        P_Cur=0
        E_Cur=5
        P1=1
        P2=2

        player=Board.create_board(self,width,height,margin,grid,P1)
        enemy=Board.create_board(self,width,height,margin,ogrid,P2)
        Sounds.play_music(1)
        Game.player_ships(self,PShips,P_Cur,self.width,self.height,self.margin,self.grid,P1)

        
        Game.opponent_ships(self,PShips,E_Cur,self.width,self.height,self.margin,self.ogrid,P2)
        Board.display_boards(self,self.width,self.height,self.margin,self.grid,self.ogrid,P1,P2)
        Game.start_game(self,PShips,self.width,self.height,self.margin,self.grid,self.ogrid,self.plyr)

    def opponent_ships(self,Ships,Current,Width,Height,Margin,Grid,Player):
        border=10
        tplaced=Current
        total=10
        Message.notifications(1)
        valid=False

        
        while tplaced<total:


            hp=Ship.get_health(Ships,Current)
            #print ("Health: ",hp)
            
            identification=Ships.ID[Current]
         #   print ("Current ID: ",Current,identification)
            placed=False
            x=random.randint(0,9)
            y=random.randint(0,9)
            direction=random.randint(0,1)
            col= y
            row= x
            
            
            try:

                    
                    
                    Board.reset_highlight(self,Grid)
                    #print ("Reset complete")
                    #for length in range(hp):
                    if direction==0:#Horizontal ship)
                        if row+hp>border:
                            valid= False
             
                        elif row+hp<=border:


                            for length in range(hp):
                               # print ("row and length ",row,length)
                                if Grid[row+length][col]!=EMP:
                                   # print("Invalid at ",row+length,col)
                                   # print (Grid[row+length][col])
                                    if 5<=Grid[row+length][col]<=9:
                                        valid=False
                                    else:
                                      #  print ("changing to invalid",row+length,col)
                                        Grid[row+length][col]=INV
                                        valid=False
                                    break
                                        
                                elif Grid[row+length][col]==EMP:
                                   # print ("Horizontal placement at ",row,col)
                                    Grid[row+length][col]=HLD

                                    valid=True
                                    
                       
                            
                    elif direction==1:#Vertical ship
                    
                        if col+hp>border:
                            valid= False
                        elif col+hp<=border:   
                            #print("Out of range")
                            for length in range(hp):
                                #print ("col and length ",col,length)
 
                                if Grid[row][col+length]!=EMP:
                                   # print("Invalid at ",row,col+length)
                                   # print(Grid[row][col+length])
                                    if 5<=Grid[row][col+length]<=9:
                                        valid=False
                                    else:
                                     #   print ("changing to invalid",row,col+length)
                                        Grid[row][col+length]=INV
                                        valid=False
                                    break
                                        

                        
                                elif Grid[row][col+length]==EMP:
                                   # print ("Vertical placement at ",row,col)
                                    Grid[row][col+length]=HLD

                                    valid=True

                
                    if valid==True:
                        #print ("ID: ",identification)
                        Board.set_ship(self,Grid,identification)
                        #print ("Placed Enemy ship at ", row,col)
                        placed=True
                        
                        if placed==True:
                            #print("getting new ship")
                            tplaced= tplaced+1
                            Current=Board.placement_check(self,tplaced,total)
                            #print ("Current and ID: ",Current,identification)
                            #print("Total placed: ",tplaced, " out of ", total)
                            valid=False

                    

                    enemy=Board.create_board(self,Width,Height,Margin,Grid,2)

                    
                    
            except IndexError:
                print("Oops! invalid coordinates. ",row,col)
  


    def player_ships(self,Ships,Current,Width,Height,Margin,Grid,Player):
        #print (Player)
        message=1
        direction=0
        highlight=False
        border=10
        tplaced=0
        total=5

        valid=False
        
        while True:
            # --- Main event loop
            name=Ship.get_ship(Ships,Current)
            hp=Ship.get_health(Ships,Current)
            identification=Ships.ID[Current]
            
            placed=False
            for event in pygame.event.get():
                pos= pygame.mouse.get_pos()
                row = pos[0] // (Height + Margin)#locates row the position is in by dividing it by the width
                col = pos[1] // (Width + Margin)#locates the column the position is by dividing it by the height

                if event.type == pygame.QUIT:#Quit
                    pygame.quit();
                try: 
                    if event.type==pygame.KEYDOWN:
                            if pygame.key.get_pressed()[pygame.K_SPACE]==True:
                                if direction==0: 
                                    direction=1
                                    #print ("placement is Vertical")

                                    message=2
                                    
                                elif direction==1:
                                    direction=0
                                    #print ("placement is Horizontal")

                                    message=3

                            if pygame.key.get_pressed()[pygame.K_RETURN]==True:
                                #print ("VALID IS CURRENTLY AT: ", valid, " AND HIGHLIGHT IS ",highlight, " AND PLACED IS ",placed)
                                #print("Return pressed")
                                ##If the selected position is invalid, inform the user
                                if valid==False:

                                    message=4

                                elif valid==True:
                                    Board.set_ship(self,Grid,identification)
                                    placed=True
                                    valid=False
                                if placed==True:
                                    tplaced= tplaced+1
                                    Current=Board.placement_check(self,tplaced,total)
                                    #print ("Current and ID: ",Current,identification)

                                    message=1
                                    
                                    if tplaced==total:

                                        return


                                  



                                    
                    if event.type== pygame.MOUSEBUTTONDOWN and highlight==True:
                        Board.reset_highlight(self,Grid)
                        #print ("Row: ",row," Col: ",col)
                        #print ("Reset complete")
                        if message==4:###This will reset the message to 1 if the previous message displayed the invalid placement message
                            message=1

                        for length in range(hp):
                            
                            if direction==0:#Horizontal ship)
                                if row+hp>border or Grid[row+length][col]!=EMP:    
                                    #print("Out of range")
                                    for length in range(hp):
                                        if 0<=Grid[row+length][col]<=4:
                                            valid=False
                                        else:
                                            Grid[row+length][col]=INV
                                            valid=False
                     
                                elif row+hp<=border:
                                    
                                    Grid[row+length][col]=HLD

                                    valid=True
                                    
                            elif direction==1:#Vertical ship
                            
                                if col+hp>border or Grid[row][col+length]!=EMP:    
                                    #print("Out of range")
                                    for length in range(hp):
                                        if 0<=Grid[row][col+length]<=4:
                                            valid=False
                                        else:
                                            Grid[row][col+length]=INV
                                            valid=False

                                elif col+hp<=border:
                                    Grid[row][col+length]=HLD

                                    valid=True
                            
                    elif event.type== pygame.MOUSEBUTTONDOWN and highlight==False:
                        if pos[0]<351 or pos[1]<351:


                            if message==4:###This will reset the message to 1 if the previous message displayed the invalid placement message
                                message=1
                            ##This will highlight based on ship size
                            for length in range(hp):
                                if direction==0:#Horizontal ship
                                    if row+hp>border or Grid[row+length][col]!=EMP:    
                                        #print("Out of range")
                                        for length in range(hp):
                                            if 0<=Grid[row+length][col]<=4:
                                                valid=False
                                            else:
                                                Grid[row+length][col]=INV
                                                valid=False
                                        
                                    else:
                                        Grid[row+length][col]=HLD

                                        highlight=True
                                        valid=True
                                        
                                elif direction==1:#Vertical ship    
                                    if col+hp>border or Grid[row][col+length]!=EMP:    
                                        #print("Out of range")
                                        for length in range(hp):
                                            if 0<=Grid[row][col+length]<=4:
                                                valid= False
                                            else:
                                                Grid[row][col+length]=INV
                                                valid=False
                                        
                                    else:
                                        Grid[row][col+length]=HLD

                                        highlight=True
                                        valid=True
                     
                            
                            
         
                    Message.instructions(message,name)
                    player=Board.create_board(self,Width,Height,Margin,Grid,1)
                    
                    Board.update_board()
                except IndexError:
                    print("Oops! mouse cursor is out of range.  Try again...")
                             
 
                screen.blit(background, [0, 0])
        # --- Limit to 60 frames per second
            clock.tick(60)


    def player_attack(self,Ships,Width,Height,Margin,Grid):
        
        while True:
            for event in pygame.event.get():
                    pos= pygame.mouse.get_pos()
                    row = pos[0]// (Width+Margin)-15#locates column the position is in by dividing it by the width minus 15 to ensure the grid stays 9x9
                    col = pos[1] // (Height + Margin)#locates the row the position is by dividing it by the height
                    fire=0
                    strike=1
                    destroy=2
                    Hit=False



                    if event.type == pygame.QUIT:#Quit
                        pygame.quit();
                    try:
                        

                        if event.type== pygame.MOUSEBUTTONDOWN:
                            #print ("Position: ",pos)
                            
                            if 525<=pos[0]<=875 and 0<= pos[1]<=350 and Grid[row][col]<13:
                                #print ("Clickity Click",pos, col,row)

                                Sounds.play_sound(fire)
                                time.sleep(1.3)

                                if 5<=Grid[row][col]<=9:
                                    
                                    Target=Grid[row][col]
                                    #print("Target is ",Target)
                                    name=Ship.get_ship(Ships,Target)
                                   # print("NAME IS ",name)

                                     
                                    
                                    hp=Ship.get_health(Ships,Target)
                                   # print ("Current Health ",hp)
                                   
                                    hp=hp-1
                                    Ship.set_health(self,Ships,Target,hp)
                                    Damage=Grid[row][col]=HIT+Target
                                    #print("TARGET ",Target)
                                   # print ("New Health ",hp)
                                    Message.attack_command(2,row,col,1,name)
                                    if hp==0:
                                        
                                        Board.Destroyed(self,Grid,Damage)
                                        message=3
                                        
                                        #OGrid[row][col]=DES
                                        Sounds.play_sound(destroy)
                                        Message.attack_command(message,row,col,1,name) 
                                    else:
                                        
                                        Sounds.play_sound(strike)
                                    Hit=True   
                                     
                                else:
                                    Grid[row][col]=MISS
                                    Hit=False
                                    #message=7
                                    name="Space"
                                    
                                    Message.attack_command(1,row,col,1,name)
                                
                                return Hit

                    
                    except IndexError:
                        print("Oops! Index value is out of range.  Try again...")
    def opp_attack(self,Ships,Width,Height,Margin,Grid):
        




        fire=0
        strike=1
        destroy=2
        Hit=False
        
        #print ("STARTING OPPONENT'S ATTACK")
        while True:
            x=random.randint(0,9)
            y=random.randint(0,9)
            direction= random.randint(0,1)
            movement=random.randint(0,1)
            row= x
            col= y
            move=movement

            
            #name=

            try:

                #print ("x is ",row, " y is ",col)
                #print (Grid[row][col])
                if Grid[row][col]==MISS or Grid[row][col]>=HIT or Grid[row][col]==DES:
                    
                    #print ("Already been targetted, retargetting")
                    Hit=False#This is to reset the method if a area has already been targetted
                else:
                    Sounds.play_sound(fire)
                    time.sleep(1.3)
                    if 0<=Grid[row][col]<=4:

                        Target=Grid[row][col]
                        #print("Target: ",Target)
                        hp=Ship.get_health(Ships,Target)
                        #print ("Current Health ",hp)

                        name=Ship.get_ship(Ships,Target)
                        #print("NAME IS ",name)
                        hp=hp-1
                        Ship.set_health(self,Ships,Target,hp)
                        Damage=Grid[row][col]=HIT+Target

                        Hit=True
                        Message.attack_command(2,row,col,2,name) 
                        if hp==0:
                            Board.Destroyed(self,Grid,Damage)
                            Message.attack_command(3,row,col,2,name)             
                            Sounds.play_sound(destroy)
                                            
                        else:           
                            Sounds.play_sound(strike)

                        ###INTELLIGENT ATTACK###4

                            #Target=Grid[row][col]
                        

      
                    elif Grid[row][col]==EMP:
                        Grid[row][col]=MISS
                        Hit=False
                        name="Space"
                        Message.attack_command(1,row,col,2,name)  

                            
                    
                    Attack_Pos.set_pos(self,row,col)
                    Attack_Pos.set_movement(self,movement)
                    Attack_Pos.set_direction(self,direction)
                    #print ("Enemy Attack finished")
                    return Hit
                    
                    
                    



            
            except IndexError:
                print ("SOMETHING WENT WRONG DURING THE ENEMY'S ATTACK!")

"""This checks the AI's attack movement when performing the intelligent attack. If the next square is out of range, it will attack a random square instead"""
    def attack_movement(self,row,col,direction,move):
        moving=True
        #print ("COMMENCING ATTACK MOVEMENT")
        if direction==0:
            dire=row
            if move==0:
                if dire-1<0:
                    #print ("Reached the left edge. Randomly attacking again")
                    moving=False
                   
                else:
                    dire=dire-1
                    row=dire

            elif move==1:
                if dire+1>9:
                    #print ("Reached the right edge. Randomly attacking again")
                    moving=False
                 
                else:
                    dire=dire+1
                    row=dire
        elif direction==1:
            dire=col
            if move==0:
                if dire-1<0:
                    #print ("Reached the top edge. Randomly attacking again")
                    moving=False
                else:
                    dire=dire-1
                    col=dire

            elif move==1:
                if dire+1>9:
                   #print ("Reached the bottom edge. Randomly attacking again")
                    moving=False
                else:
                    dire=dire+1
                    col=dire
        Attack_Pos.set_pos(self,row,col)
        Attack_Pos.set_movement(self,move)
        Attack_Pos.set_direction(self,direction)
        #print("FINISHED ATTACK MOVEMENT")
        return moving
    
    """This is an improvement to the original AI attack. This method provides the AI with a little 'common sense'.
    If the previous attack was a hit, it will attack in a random vertical or horizontal line.
    If the direction it tries to attack has not been attacked already the AI will keep firing in that direction until it misses.
    If the attack was has already been targetted before, it will choose a random square instead."""
    def opp_attack_intel(self,Ships,Width,Height,Margin,Grid,Col,Row):
            x=random.randint(0,9)
            y=random.randint(0,9)
            fire=0
            strike=1
            destroy=2
            Hit=False
            row=Row
            col=Col



            try:
              #  print ("Row is: ", row, " and Col is ",col)
                Target=Grid[row][col]
                Sounds.play_sound(fire)
                time.sleep(1.3)
                if 0<=Target<=4:
                   # print("Target: ",Target)
                    hp=Ship.get_health(Ships,Target)
                    #print ("Current Health ",hp)
                    hp=hp-1
                    Ship.set_health(self,Ships,Target,hp)
                    Damage=Grid[row][col]=HIT+Target
                   # print("TARGET of damaged ship",Damage)
                    #print ("New Health ",hp)
                    Hit=True
                    if hp==0:
                        Board.Destroyed(self,Grid,Damage)
                                    
                        Sounds.play_sound(destroy)
                                        
                    else:           
                        Sounds.play_sound(strike)
                    


                elif Grid[row][col]==EMP:
                  #  print ("FINALLY MISSES HERE")
                    Grid[row][col]=MISS
                    Hit=False
               # print ("FINISHED ENEMY INTEL ATTACK")
                return (Hit)
    
                            
            except IndexError:
                print ("SOMETHING WENT WRONG DURING THE ENEMY'S ATTACK!")
                
"""This gets the total health of all ships still functioning. This is used to determine when a player has won by identifying how many ships
remain that haven't been successfully destroyed"""
    def get_total_health(self,ships,player):
        #print("Player: ",player)
        count=0
        total=0
        if player==1:
            for count in range(5,10):
                total=total+Ship.get_health(ships,count)
                #print("P1: ",total)
            return total
        elif player==2:
            for count in range(0,5):
                total=total+Ship.get_health(ships,count)
                #print("P2: ",total)
            return total
        
"""This is the start game method. It is the main loop for the game."""        
    def start_game(self,Ships,Width,Height,Margin,Grid,OGrid,Plyr):
        turn=Player.set_turn(self,Plyr)
        victory=False
        


        while victory!=True:

                player=Player.get_turn(self)


            # --- Main Game Event loop
            
            
                screen.blit(background, [0, 0])##Blit background to remove previous text
                try:
                    #if victory==True:
                    while player==1:
                        if Game.player_attack(self,Ships,Width,Height,Margin,OGrid)==True:
                            #print ("HIT")
                            
                            player=1
                            Board.display_boards(self,Width,Height,Margin,Grid,OGrid,1,2)
                            #print(Game.get_total_health(self,Ships,player))
                            if Game.get_total_health(self,Ships,player)==0:
                               # print ("You Won!")
                                Message.notifications(3)
                                victory=True
                                Sounds.play_music(3)
                                break
                        else:
                            #print ("Missed.Changing Player's turn from player")

                            Player.set_turn(self,player)
                            
                            break
                       


                            
                        #Message.instructions(message,name)
                    while player==2:

                            screen.blit(background, [0, 0])##Blit background to remove previous text
                            if Game.opp_attack(self,Ships,Width,Height,Margin,Grid)==True:
                                    if Game.get_total_health(self,Ships,player)==0:
                                      #  print ("You Lost!")
                                        Message.notifications(2)
                                        victory=True
                                        Sounds.play_music(2)
                                        break

                                    #print("Enemy's go.")


                                    attack=True
                                   
                                    player=2
                                    Board.display_boards(self,Width,Height,Margin,Grid,OGrid,1,2)
                                   # print("Health remaining ",Game.get_total_health(self,Ships,player))
                                    while attack!=False:
                                        Board.display_boards(self,Width,Height,Margin,Grid,OGrid,1,2)
                                        row=Attack_Pos.get_pos(self)[0]
                                        col=Attack_Pos.get_pos(self)[1]
                                        direction=Attack_Pos.get_direction(self)
                                        move=Attack_Pos.get_movement(self)
                                        if Game.attack_movement(self,row,col,direction,move)==True:
                                            row=Attack_Pos.get_pos(self)[0]#These update the positions
                                            col=Attack_Pos.get_pos(self)[1]#
                                            direction=Attack_Pos.get_direction(self)#
                                            move=Attack_Pos.get_movement(self)#
                                           # print("Row ",row, " Col ",col, direction,move)
                                            if Grid[row][col]<=10:
                                              #  print ("x is ",row, " y is ",col)
                                               # print ("TESTING!")
                                                
                                                #print(Attack_Pos.get_pos(self)[0])
                                                if Game.opp_attack_intel(self,Ships,Width,Height,Margin,Grid,col,row)==True:
                                                  #  print ("THE ATTACK CONTINUES!")
                                                    attack=True
                                                    

                                                    
                                                    if Game.get_total_health(self,Ships,2)==0:
                                                        attack=False
                                                        
                                                        
                                                else:
                                                  #  print("Missed")
                                                    attack=False
                                                    Player.set_turn(self,player)
                                                    
                                                    

                                            else:
                                                #print("Invalid attack. Resetting")
                                               # print (Grid[row][col],"Row ",row," Col ",col)
                                                attack=False

                                        else:
                                            attack=False
                                    if attack==False:
                                        break
                                   

                            else:
                                #print ("Changing to player 1")
                                Player.set_turn(self,player)
                                
                                #print ("Missed.Changing Player's turn from enemy")
                                
                                break

                    
                    Board.display_boards(self,Width,Height,Margin,Grid,OGrid,1,2)

                    
                except IndexError:
                    print("Oops! There is an index error in regards to the players.")
                               
class execute:
    def on_execute(self):
        Game()
        pass

 
if __name__ == "__main__" :
    theApp = execute()
    theApp.on_execute()           

