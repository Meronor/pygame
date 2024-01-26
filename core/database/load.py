import ast
import sqlite3


def load():
    try:
        with sqlite3.connect("core\database\\all_data") as con:
            cur = con.cursor()
            return ast.literal_eval('{' + cur.execute(f"SELECT lib FROM load").fetchall()[0][0] + '}')
    except Exception as s:
        print(s)
        print('load')
        return False


def save(hero_cords, bg_image, wb_bg_image, all_sprites, objects, inventory):
    with sqlite3.connect("core\database\\all_data") as con:
        cur = con.cursor()
        try:
            cur.execute(
                f'UPDATE load SET lib = "' + f"'hero_cords': '{hero_cords}','bg_image':'{bg_image}',"
                f"'wb_bg_image': '{wb_bg_image}', 'all_sprites': '{all_sprites}',"
                                            f"'objects': '{objects}','inventory': '{inventory}'" + '"')
        except Exception as s:
            print(s)
            print('save')
        return False
