import os, requests, base64, time, sys, shutil
from Frontend.MySQLconnect import get_db
from Frontend import IMG_FOLDER
from io import BytesIO
from matplotlib.figure import Figure


EXT = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'}
cache_host = "http://3.143.22.33:5001"

def get_cache_parameter():
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered=True)

        query = '''SELECT * FROM config WHERE ctime = (SELECT MAX(ctime) FROM config LIMIT 1)'''
        cursor.execute(query)

        if (cursor._rowcount):
            cache_para = cursor.fetchone()
            return cache_para
        else:
            return None

    except:
        return None

def set_cache_parameter(cap, strategy):
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered=True)
        ctime = time.time() - 18000

        query_add = ''' INSERT INTO config (ctime, cap, strategy) VALUES (%s,%s,%s)'''
        cursor.execute(query_add, (ctime, cap, strategy))
        cnx.commit()
        return "success"

    except:
        return None

def set_status(size, item_count, request_count, miss_count):
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered=True)

        query_add = ''' INSERT INTO stats (size, item_count, request_count, miss_count) VALUES (%s,%s,%s,%s)'''
        cursor.execute(query_add, (size, item_count, request_count, miss_count))
        cnx.commit()
        return None

    except:
        return None

def save_image(request, key):
    global cache_host

    file = request.files['file']
    name, ex = os.path.splitext(file.filename)

    if ex.lower() in EXT and sys.getsizeof(file) < 2097152:
        filename = key + ex

        file.save(os.path.join(IMG_FOLDER, filename))
        j = {"key": key}
        res = requests.post(cache_host + '/invalidate', json=j)

        return write_img_to_db(key, filename)

    return "invalid"

def clear_folder():
    for filename in os.listdir(IMG_FOLDER):
        path = os.path.join(IMG_FOLDER, filename)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            return None

    return "success"

def clear_db():
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered=True)

        query_delete= '''DELETE FROM img'''
        cursor.execute(query_delete)
        cnx.commit()
        return "success"

    except:
        return None

def base64_img(filename):
    with open(IMG_FOLDER + "/" + filename, "rb") as img_path:
        img = img_path.read()
        base64_img = base64.b64encode(img)
    img = base64_img.decode('utf-8')
    return img

def write_img_to_db(ikey, ipath):
    if ikey == "" or ipath == "":
        return "fail"

    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        q_exist = "SELECT EXISTS(SELECT ikey FROM img WHERE ikey=(%s))"
        cursor.execute(q_exist, (ikey,))

        for i in cursor:
            if i[0] == 1:
                q_delete = '''DELETE FROM img WHERE ikey=%s'''
                cursor.execute(q_delete, (ikey,))
                break

        q_add = ''' INSERT INTO img (ikey, ipath) VALUES (%s, %s)'''
        cursor.execute(q_add, (ikey,ipath))
        cnx.commit()
        cnx.close()
        return "ok"

    except:
        return "fail"

def plot_graphs(data_x_axis, data_y_axis, y_label):

    fig = Figure()
    ax = fig.subplots()
    ax.plot(data_x_axis, data_y_axis)
    ax.set(xlabel='Time (every 5 seconds)', ylabel=y_label)

    fig.autofmt_xdate()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot = base64.b64encode(buf.getbuffer()).decode("ascii")

    return plot

