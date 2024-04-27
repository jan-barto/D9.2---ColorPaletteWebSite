from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdef"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
bootstrap = Bootstrap5(app)


def provide_list_of_colors(path, amount_of_colors, delta):
    image = Image.open(path)
    image.thumbnail((600, 400))
    arr = np.array(image)

    flatten = arr.reshape(-1, arr.shape[-1])
    unique_arr, counts_arr = np.unique(flatten, axis=0, return_counts=True)
    sorted_indices = np.argsort(counts_arr)[::-1]
    unique_arr_sorted = unique_arr[sorted_indices]
    unique_arr_sorted = [tuple(color) for color in unique_arr_sorted]

    unique_colors_list = [unique_arr_sorted[0]]
    for color in unique_arr_sorted:
        is_different = False
        for colorx in unique_colors_list:
            diff_r = abs(int(color[0]) - int(colorx[0]))
            diff_g = abs(int(color[0]) - int(colorx[0]))
            diff_b = abs(int(color[0]) - int(colorx[0]))
            total = diff_r + diff_g + diff_b
            if total > delta:
                is_different = True
                # print(color, colorx, total, delta)

        if is_different:
            unique_colors_list.append(color)

        if len(unique_colors_list) >= amount_of_colors:
            break

    top_colors_list = ['#{:02x}{:02x}{:02x}'.format(item[0], item[1], item[2]) for item in unique_colors_list]
    print(unique_colors_list)
    print(top_colors_list)
    image.close()
    return top_colors_list


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("Validation passed.")
        file = request.files['picture']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "temp_img"))
            file_set = "static/uploads/temp_img"
        else:
            file_set = "static/def_img.jpg"

        colors_num = request.form.get('colors_num')
        delta = request.form.get('delta')
        colors = provide_list_of_colors(file_set, int(colors_num), int(delta))

        setting = {
            'colors_num_set': colors_num,
            'delta_set': delta,
            'file_set': file_set
        }
        return render_template("index.html", setting=setting, colors=colors)

    setting = {
        'colors_num_set': 10,
        'delta_set': 200,
        'file_set': "static/def_img.jpg"
    }
    return render_template("index.html", setting=setting)


if __name__ == '__main__':
    app.run(debug=True)
