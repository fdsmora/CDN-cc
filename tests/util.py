def count_logfile_lines(logfile):
    total_lines_count = 0
    with open(logfile, 'r') as f:
        total_lines_count =  count_lines(f) - 2 # discount header lines
    return total_lines_count

def count_lines(file_handle):
    for i,line in enumerate(file_handle):
        pass
    return i+1

def count_log_records_in_db(db):
    row = db.execute('SELECT COUNT(*) FROM LOGS').fetchone()    
    return row[0]

