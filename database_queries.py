from db_connection import create_connection, get_cursor
import mysql.connector


#Character list return

def character_list():
    
    characters = {}
    
    try:
        connection = create_connection()
        cursor = get_cursor(connection)
    except mysql.connector.Error as err:
                print(f"Error: {err}")
    
    characters_display_query = f'''
    SELECT * FROM characters
    '''
    
    cursor.execute(characters_display_query)
    rows = cursor.fetchmany(size=20)   

    for char_id, name in rows:
        characters[char_id] = name
    
    
    
    return characters


#character moveset return with frame data response

tables = ['normals', 'command_normals', 'target_combos', 'throws', 'drive_system', 'special_moves', 'super_arts', 'taunts', 'serenity_stance']

def character_moveset_fetch(id: int, name: str):
    
#First, we create the dictionaries that are going to receive the info from the database
    
    if name != 'Chun-Li':
    
        character_moveset = {
                            'character': f'{name}',
                            'normals': {},
                            'command_normals': {},
                            'target_combos': {},
                            'throws': {},
                            'drive_system': {},
                            'special_moves': {},
                            'super_arts': {},
                            'taunts': {}
                            }
    else:
        
        character_moveset = {
                            'character': f'{name}',
                            'normals': {},
                            'command_normals': {},
                            'target_combos': {},
                            'throws': {},
                            'drive_system': {},
                            'special_moves': {},
                            'super_arts': {},
                            'taunts': {},
                            'serenity_stance': {}
                            }
        

#Then, we connect to the db to retrieve the info.

    try:
        
        connection = create_connection()
        cursor = get_cursor(connection)
        
        
        for move_type in tables:
            character_moveset_fetch = f'''
                SELECT move_name, move_nomenclature, startup, active_f, recovery, cancel, damage, guard, on_hit, on_block FROM {move_type}
                WHERE character_id = {id};
                '''
            cursor.execute(character_moveset_fetch)
            moveset = cursor.fetchall()

            for move_name, move_nomenclature, startup, active_f, recovery, cancel, damage, guard, on_hit, on_block in moveset:
                
                if move_type == 'serenity_stance' and name != 'Chun-Li':
                    continue
                
                 
                inner_moveset = {f'{move_name}': {
                    'nomenclature' : f'{move_nomenclature}',
                    'startup' : f'{startup}',
                    'active_f' : f'{active_f}',
                    'recovery' : f'{recovery}',
                    'cancel' : f'{cancel}',
                    'damage' : f'{damage}',
                    'guard' : f'{guard}',
                    'on_hit' : f'{on_hit}',
                    'on_block' : f'{on_block}'
                    }
                }
                
                new_inner_moveset = {move_name: [attributes] for move_name, attributes in inner_moveset.items()}

                character_moveset[move_type].update(new_inner_moveset)
                
                 
                
        return character_moveset
                
            
    except mysql.connector.Error as err:
                print(f"Error: {err}")
                

#function to retrieve the id of characters for the queries for just a single type of move

def retrieve_id(name: str):
    
    try:
        
        connection = create_connection()
        cursor = get_cursor(connection)
        
        id_query = f'''
        SELECT id from characters
        WHERE character_name = '{name.upper()}';
        '''
    
        cursor.execute(id_query)
        id_char = cursor.fetchone()
        
        cursor.close()
        connection.close() 
        
        return id_char[0] 
        
    except mysql.connector.Error as err:
                print(f"Error: {err}")    
                

            
        
        
        
                
    

    
    
    
    
    
    