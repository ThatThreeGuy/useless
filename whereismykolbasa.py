from kolbasa_props import *


WHITE = (225, 225, 225)

plr = player('mc_stand_back.png', 250, 200, PLR_SIZE)
shotgun = basicsprite('shotgun_first_person.png', 100, 100, (300, 150))
snipe = basicsprite('snipe.png', 0,0, (50, 50))
background = basicsprite('kitchen_bg.png', 0, 0, WND_SIZE)
dialogue = basicsprite('dlg_prot.png', 0, 0, (WND_SIZE[0], 150))
dialogue_face = basicsprite('face_normal.png', 35, 30, (75, 100))
kolbasa = basicsprite('the_kolbasa_in_question.png', 250, 250, (100, 100))
chefs_table = basicsprite('chef_table.png', 0,0, WND_SIZE)
enter = basicsprite('enter.png', plr.rect.x, plr.rect.y, (175, 175))
lvls_interactable_objs = { 0:{
    (0,400): 'dialogue', (600, 400):'fun dialogue'}
}
point_on = None
locked_door = basicsprite('tutorial_door.png', 200, 0, (300, 500))

mc_face_sprites = [
    transform.scale(image.load('face_normal.png'), (75, 100)), ### 0
    transform.scale(image.load('face_bruh.png'), (75, 100)), ### 1
    transform.scale(image.load('face_cry.png'), (75, 100)), ### 2
    transform.scale(image.load('face_sus.png'), (75, 100)), ### 3
    transform.scale(image.load('face_ugh.png'), (75, 100)), ### 4
]
def dlg(t, face_sprite = mc_face_sprites[0], pos = 'up'):
    global game
    whole_text = ''
    to_continue = False
    dialogue_face.image = face_sprite
    if pos == 'up':
        dialogue.rect.x = 0
        dialogue.rect.y = 0
        dialogue_face.rect.y = 30
    if pos == 'down':
        dialogue.rect.y = WND_SIZE[1] - 150
        dialogue.rect.x = 0
        dialogue_face.rect.y = 375


    dialogue.render()
    dialogue_face.render()

    fontt = font.SysFont('verdana', 30)
    for i in t:
        whole_text += i
        if pos == 'up':
            if len(whole_text) <= 25:
                wnd.blit(fontt.render(whole_text, True, WHITE), (210, 15))
            if len(whole_text) > 25:
                wnd.blit(fontt.render(whole_text[25:len(whole_text)], True,WHITE), (200, 50))
        if pos == 'down':
            if len(whole_text) <= 25:
                wnd.blit(fontt.render(whole_text, True, WHITE), (210, 375))
            if len(whole_text) > 25:
                wnd.blit(fontt.render(whole_text[25:len(whole_text)], True,WHITE), (200, 410))
        clock.tick(15)
        display.update()
    while to_continue == False:
        for ev in event.get():
            if ev.type == QUIT:
                game = False
            if ev.type == KEYDOWN:
                if ev.key == K_RETURN:
                    to_continue = True
        if game == False:
            break
        clock.tick(30)
        display.update()
#### DLG
def enter_control(): ### це пздц
    keys = key.get_pressed()
    if keys[K_RETURN] and enter.rect.x == plr.rect.x:
        if lvls_interactable_objs[plr.level_on][point_on] == 'dialogue': ### для сужетных диалогов
            plr.talk += 0.5
        if lvls_interactable_objs[plr.level_on][point_on] == 'fun dialogue': ### для диалогов-пасхалок (так же удобно как есть пиццу вилкой и ножом когда вилка и нож горят)
            if plr.level_on == 0:
                dlg('Всегда знал что никто не любит ходить на лево', mc_face_sprites[4])
                del lvls_interactable_objs[plr.level_on][point_on]
                


    

while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        if ev.type == MOUSEBUTTONDOWN and gamemode == 'shotgun' and shotgun_reload_time <= 0:
            shotgun.image = shotguns_anims[1]
            shotgun_reload_time = 20
            if plr.level_on == 0:
                if Rect.colliderect(locked_door.rect, snipe.rect):
                    dlg('Бум')
                    plr.level_on = 0.5
                elif tutorial_missed_shots == 0:
                    dlg('Ладно.. с кем не бывает',mc_face_sprites[1])
                    tutorial_missed_shots += 1
                elif tutorial_missed_shots == 1:
                    dlg('...', mc_face_sprites[1])
                    tutorial_missed_shots += 1
                elif tutorial_missed_shots == 2:
                    dlg('Ещё раз промажешь я закрою игру', mc_face_sprites[1])
                    tutorial_missed_shots += 1
                elif tutorial_missed_shots == 3:
                    dlg('Доигрался')
                    game = False
                

    #wnd.fill(WHITE)

    if gamemode == 'basic':
        enter.is_on_screen = False
        background.render()
        plr.control()
        plr.render()

    
        for pos in lvls_interactable_objs[plr.level_on]:
            if plr.collpoint(pos[0], pos[1]):
                enter.rect.x = plr.rect.x
                enter.is_on_screen = True
                point_on = pos

        if enter.is_on_screen:
            enter_control()
            enter.render()

        


        if plr.talk == 1:
            plr.image = plr_stand_back
            plr.render()
            dlg('...')
            dlg('Грохочет гром..')
            dlg('Сверкает молния в ночи..')
            dlg('А на холмеееее')
            dlg('...', mc_face_sprites[1])
            dlg('У меня нет колбасы', mc_face_sprites[2])
            chefs_table.render()
            dlg('Кто бы мог подумать', mc_face_sprites[2])
            chefs_table.render()
            dlg('Но если я вот таким отдам заказ', mc_face_sprites[0], 'down')
            dlg('То не увижу своих кровью и потом заработаных денек', mc_face_sprites[4], 'down')
            dlg('...', mc_face_sprites[4], 'down')
            dlg('Ладно, жить ещё на что-то надо.', mc_face_sprites[4], 'down')
            dlg('В путь')
            plr.talk += 0.5
        if plr.talk == 2:
            dlg('...')
            dlg('Ватафак', mc_face_sprites[3])
            dlg('Дверь не открывается')
            dlg('Опять пранк?')
            dlg('Тч')
            dlg('Это может быть и смешно')
            dlg('Но я ещё не видел ничего смешнее дробовика 7-го калибра')
            wnd.fill(GRAY)
            locked_door.render()
            dlg('Главное не промазать')
            gamemode = 'shotgun'
            plr.talk += 0.5

    if gamemode == 'shotgun':
        if plr.level_on == 0: ###Фон и спрайты на экране
            wnd.fill(GRAY)
            locked_door.render()
        if plr.level_on == 0.5:
            wnd.fill(GRAY)
            locked_door.image = image.load('tutorial_door_open.png')
            locked_door.render()
            dlg('Ух... запах свободы', mc_face_sprites[0], 'down')
            dlg('Кефтеме', mc_face_sprites[0], 'down')
            plr.level_on = 1
            gamemode = 'basic'
        
        if shotgun_reload_time == 0:
            shotgun.image = shotguns_anims[0]
        m_x, m_y = mouse.get_pos()
        snipe.rect.x = m_x - 25
        snipe.rect.y = m_y -25 
        snipe.render()
        shotgun.render()
        shotgun.rect.x = m_x
        shotgun.rect.y = m_y + 25
        shotgun_wait = 120
        if shotgun_reload_time > 0:
            shotgun_reload_time -= 1

    
    clock.tick(60)
    display.update()

