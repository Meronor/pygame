import ast
import csv
import sqlite3


def save(hero_cords, bg_image, wb_bg_image, all_sprites, objects, inventory):
    try:
        with open('core\saves\\save_file.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'param']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'name': 'hero_cords', 'param': hero_cords})
            writer.writerow({'name': 'bg_image', 'param': bg_image})
            writer.writerow({'name': 'wb_bg_image', 'param': wb_bg_image})
            writer.writerow({'name': 'all_sprites', 'param': all_sprites})
            writer.writerow({'name': 'objects', 'param': objects})
            writer.writerow({'name': 'inventory', 'param' : inventory})

    except Exception as e:
        print(e)


# def load():
#     try:
#         with open("core\saves\\save_file.csv", encoding='utf-8') as f:
#             data = f.read().split('\n')
#             cur_data = []
#             for item in data:
#                 item = item.split(',')
#                 cur_data.append(item)
#             data = dict(cur_data[0:-1])
#         print(data)
#         return data
#     except Exception as e:
#         print('error:', e)
#         exit()


def load():
    try:
        with sqlite3.connect("core\database\\all_data") as con:
            cur = con.cursor()
            return ast.literal_eval('{' + cur.execute(f"SELECT lib FROM load").fetchall()[0][0] + '}')
    except Exception as s:
        print(s)
        print('load')
        return False


# def save(hero_cords, bg_image, wb_bg_image, all_sprites, objects, inventory):
#     with sqlite3.connect("core\database\\all_data") as con:
#         cur = con.cursor()
#         try:
#             cur.execute(
#                 f'UPDATE load SET lib = "' + f"'hero_cords': '{hero_cords}','bg_image':'{bg_image}',"
#                 f"'wb_bg_image': '{wb_bg_image}', 'all_sprites': '{all_sprites}',"
#                                             f"'objects': '{objects}','inventory': '{inventory}'" + '"')
#         except Exception as s:
#             print(s)
#             print('save')
#         return False
#