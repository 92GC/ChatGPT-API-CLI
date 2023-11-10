import read_write

def get_next_user_step(user_id):
    step = read_write.get_user_step(user_id)
    return step + 1
