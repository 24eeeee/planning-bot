def form_request_new_table(user_id):
    return "CREATE TABLE IF NOT EXISTS \"" + str(user_id) + \
           "\" (task_number INTEGER PRIMARY KEY AUTOINCREMENT, task text);"


def form_request_add_task(user_id, task):
    return "INSERT INTO \"" + str(user_id) + "\" (task) VALUES (\"" + task + "\")"


def form_request_delete_task(user_id, task_number):
    return "DELETE FROM \"" + str(user_id) + "\" WHERE task_number = " + str(task_number)


def form_request_show_all_tasks(user_id):
    return """SELECT rowid, task FROM \"""" + str(user_id) + "\""


def form_request_remember_deleted_task(user_id, task_number):
    return "SELECT task FROM \"" + str(user_id) + "\" WHERE task_number = " + str(task_number)


def form_request_count_elements_of_table(user_id):
    return "SELECT COUNT(*) FROM \"" + str(user_id) + "\""
