def obj_replace(obj_list):
    """pointかつcellsを2次元配列化へ整形する関数"""
    
    result = []
    target = ':'
    for obj in obj_list:
        obj = obj.replace('(', '').replace(')', '').strip()
        idx = obj.find(target)
        coordinate_obj_list = obj[idx:][1:]
        x = coordinate_obj_list.split(',')[0]
        y = coordinate_obj_list.split(',')[1]
        z = coordinate_obj_list.split(',')[2]
        result.append([x, y, z])
        
    return result


def cell_types_obj_replace(obj_list):
    """cell_typesを1次元配列化へ整形する関数"""
    
    result = []
    for obj in obj_list:
        obj.strip()
        result.append(obj.strip())
        
    return result