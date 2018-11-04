import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep
from random import randint

def check_keydown_events(event,ai_settings,stats,screen,ship,bullets,st):
    #"""��Ӧ����"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_KP0 and stats.strokes_number > 0:
        new_bullet = Bullet(ai_settings,screen,ship,True)
        bullets.add(new_bullet)
        stats.strokes_number -= 1
        strokes_list = st.strokes.sprites()
        stroke = strokes_list[0]
        st.strokes.remove(stroke)

def check_keyup_events(event,ship):
    #"""��Ӧ�ɿ�"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,st):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,stats,screen,ship,bullets,st)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cheak_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y,st)

def cheak_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y,st):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        st.prep_strokes()

def fire_bullet(ai_settings,screen,ship,bullets):
    #"""�����û�е������ƣ��ͷ���һ���ӵ�"""
    # ����һ���ӵ�����������뵽����bullets��
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship,False)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width, alien_height = alien.rect.width, alien.rect.height
    alien.x = randint(0,1200 - alien_width)
    alien.y = randint(0,alien_height)
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)

    # 创建外星人群
    if ai_settings.waitting_alien > number_aliens_x:
        for i in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens)

        ai_settings.waitting_alien -= number_aliens_x
    elif ai_settings.waitting_alien > 0:
        for i in range(ai_settings.waitting_alien):
            create_alien(ai_settings,screen,aliens)

        ai_settings.waitting_alien = 0

def cheak_fleet_edges(ai_settings,screen,ship,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            i = change_fleet_direction(ai_settings,alien)
            if i and ai_settings.waitting_alien != 0:
                create_fleet(ai_settings,screen,ship,aliens)

def change_fleet_direction(ai_settings,alien):
    """将外星人下移，并改变它们的方向"""
    alien.rect.y += ai_settings.fleet_drop_speed
    alien.fleet_direction *= -1

    if alien.rect.y > alien.rect.height:
       return True;
    else:
       return False;

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,st):
    #"""�����ӵ���λ�ã���ɾ������ʧ���ӵ�"""
    # �����ӵ���λ��
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    cheak_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,st)

def cheak_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,st):
    """响应子弹和外星人的碰撞"""

    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,False,True)

    if collisions:
        for bullet in collisions.keys():
            if bullet.rect.width == ai_settings.bullet_width_small:
                bullets.remove(bullet)
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        cheak_high_score(stats,sb)

    if len(aliens) == 0 and ai_settings.waitting_alien == 0:
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级和大招数量
        stats.level += 1
        stats.strokes_up()
        sb.prep_level()
        st.prep_strokes()

        create_fleet(ai_settings,screen,ship,aliens)

def cheak_high_score(stats,sb):
    """检查是否诞生了新的最高得分"""
    if stats.score >stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,st):
    #"""������Ļ�ϵ�ͼ�񣬲��л�������Ļ"""
    # ÿ��ѭ��ʱ���ػ���Ļ
    screen.fill(ai_settings.bg_color)
    # �ڷɴ��������˺����ػ������ӵ�
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()
    st.strokes.draw(screen)

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # ��������Ƶ���Ļ�ɼ�
    pygame.display.flip()

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
         
        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        ai_settings.waitting_alien = ai_settings.alien_number_limit

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    cheak_fleet_edges(ai_settings,screen,ship,aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

    # 检查是否有外星人抵达屏幕底端
    cheak_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def cheak_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人抵达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被外星人撞到一样处理
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def cheak_hig_score(stats,sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()