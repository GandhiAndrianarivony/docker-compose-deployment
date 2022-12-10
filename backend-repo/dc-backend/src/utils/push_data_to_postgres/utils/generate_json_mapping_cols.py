import os
import json


def get_key_mapping(fetched_data, col_mapping_path):
    file_path = os.path.join("data", col_mapping_path)
    if not os.path.isfile(file_path):
        keys = []
        keys_states = set()
        for fd in fetched_data:
            for k in list(fd.keys()):
                if k not in keys_states:
                    keys_states.add(k)
                    keys.append(
                        {
                            "mongo_key": k,
                            "postgres_key": ""
                        }
                    )
                else:
                    continue

        print(f"You file is created at : {file_path}")
        
        with open(f'{file_path}', 'w') as fw:
            fw.write(json.dumps(keys))
        return False

    return True

