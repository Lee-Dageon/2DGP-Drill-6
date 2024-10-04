from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def lerp(start, end, t): #선형 보간 함수(character의 위치를 점진적으로 변환)
    return start + (end - start) * t


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
hide_cursor()

# 처음 손의 랜덤 위치 설정
hand_x, hand_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)

# 타이머 변수 추가
time_plus = 0
time_limit = 1.0  # 1초 후에 hand 위치를 변경

# 이동 속도를 제어하는 변수
speed = 0.1  # 캐릭터가 목표로 이동하는 속도

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 랜덤 좌표에 hand 이미지 그리기
    hand.draw(hand_x, hand_y)

    # 캐릭터를 현재 위치에 그리기
    if hand_x>x:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y) #오른쪽 이미지
    elif hand_x<x:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)  # 왼쪽 이미지


    # 캐릭터가 hand의 위치로 서서히 이동 (LERP 사용)
    x = lerp(x, hand_x, speed)
    y = lerp(y, hand_y, speed)

    # 캐릭터가 거의 손의 위치에 도달했으면 (작은 오차 범위)
    if abs(x - hand_x) < 1 and abs(y - hand_y) < 1:
        # 2초 후에 hand의 새로운 랜덤 위치 생성
        time_plus += 0.5
        if time_plus >= time_limit:
            hand_x, hand_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)
            time_elapsed = 0  # 타이머 초기화

    update_canvas()

    # 프레임 전환 및 딜레이
    frame = (frame + 1) % 8 #프레임 8개
    delay(0.05)

    handle_events()

close_canvas()
