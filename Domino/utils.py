import pygame as pg
from settings import W, H, CELL_SIZE, \
    STORAGE_PANE_COORDS, DOMINO_BACKSIDE_COLOR_1, DOMINO_BACKSIDE_COLOR_2, DOMINO_BORDER_COLOR, PLAYER_WIN, CMP_WIN,\
    STANDOFF


def get_player_pool_position(player_pool):
    return W // 2 - player_pool.PANE_WIDTH // 2, H - 4 * CELL_SIZE


def get_cmp_pool_position(cmp_pool):
    return W // 2 - cmp_pool.PANE_WIDTH // 2, CELL_SIZE


def get_domino_backside():
    surface = pg.Surface((CELL_SIZE, 2 * CELL_SIZE))

    # Заполняем фон
    surface.fill(DOMINO_BACKSIDE_COLOR_1)

    # Рисуем границу
    pg.draw.rect(surface, DOMINO_BORDER_COLOR, (0, 0, CELL_SIZE, CELL_SIZE * 2), 1)

    # Получем опорные величины
    delta_x = delta_y = CELL_SIZE // 6

    # Рисуем верхний и нижний квадраты
    pg.draw.rect(surface, DOMINO_BACKSIDE_COLOR_2, (delta_x, delta_y, 4 * delta_x, 4 * delta_y))
    pg.draw.rect(surface, DOMINO_BACKSIDE_COLOR_2, (delta_x, 7 * delta_y, 4 * delta_x, 4 * delta_y))

    # Рисуем разделительную линию
    pg.draw.line(surface, DOMINO_BACKSIDE_COLOR_2, (delta_x, 6 * delta_y), (5 * delta_x, 6 * delta_y), 3)

    return surface


def check_end_game(player_pool, cmp_pool, storage):
    # Сторона, выложившая в цепочку все свои домино - побеждает
    if player_pool.is_empty:
        return PLAYER_WIN
    if cmp_pool.is_empty:
        return CMP_WIN

    # Если хранилище пусто и ни у кого нет доступных ходов - ничья
    if storage.is_empty and not is_available_moves(player_pool) and not is_available_moves(cmp_pool):
        return STANDOFF

    return None


def is_available_moves(pool):
    for domino in pool.domino_list:
        available_for_left, available_for_right = check_available_for_domino(domino, pool.chain)
        if available_for_left or available_for_right:
            return True
    return False


def check_available_for_domino(domino, chain):
    available_for_left = domino.side1 == chain.left_side or domino.side2 == chain.left_side
    available_for_right = domino.side1 == chain.right_side or domino.side2 == chain.right_side
    return available_for_left, available_for_right


def draw_chain(surface, chain, scope):
    if chain.width < W:
        scope.move_to_line(chain.center_line)
    chain.create_surface(scope)
    surface.blit(chain.surface, (0, 0))


def draw_storage_pane(surface, storage):
    storage.create_surface()
    surface.blit(storage.surface, STORAGE_PANE_COORDS)


def draw_player_pool(surface, player_pool):
    player_pool.create_surface()
    x, y = get_player_pool_position(player_pool)
    surface.blit(player_pool.surface, (x, y))


def draw_cmp_pool(surface, cmp_pool):
    cmp_pool.create_surface()
    x, y = get_cmp_pool_position(cmp_pool)
    surface.blit(cmp_pool.surface, (x, y))


def draw_game_result(surface, game_result):
    surface.blit(game_result.surface, (0, 0))

def is_quit_event(events):
    for event in events:
        if event.type == pg.QUIT:
            return True
    return False


def quit_game():
    pg.quit()
    exit()

