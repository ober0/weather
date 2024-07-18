import pprint
from get_weather import get_weather
from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify

app = Flask(__name__)



@app.route('/')
def index():
    viewed_cities = []
    time = request.args.get('time')
    if not time:
        time = 'today'
    try:
        city = request.cookies.get('user_city')
        viewed_city = request.cookies.get('viewed_city')
        if not city:
            city = 'Москва'
        if viewed_city:
            if len(viewed_city.split('/')) > 5:
                viewed_city = list(set(viewed_city.split('/')))
                viewed_cities = viewed_city[-1:-6:-1]

            else:
                viewed_city = list(set(viewed_city.split('/')))
                viewed_cities.extend(viewed_city[::-1])

    except:
        city = 'Москва'

    try:
        search_city = request.args.get('city')
        if search_city:
            city = search_city
            weather = get_weather(city, time)

            resp = make_response(render_template('index.html', weather=weather, city=city, viewed_cities=viewed_cities, time=time))
            resp.set_cookie('user_city', city)

            return resp
    except:
        pass
    weather = get_weather(city, time)
    return render_template('index.html', weather=weather, city=city, viewed_cities=viewed_cities, time=time)


@app.route('/changeCity', methods=['POST'])
def changeCity():
    city = request.json.get('city')
    try:
        if get_weather(city, 'today'):
            resp = make_response(jsonify({
                'success': True,
            }))
            resp.set_cookie('user_city', city)
            try:
                viewed_city = request.cookies.get('viewed_city').split('/')
                print(viewed_city)
                if len(viewed_city) > 5:
                    viewed_city = viewed_city[-1:-5:-1][::-1]
                viewed_city.append(city)
                coockie_data = '/'.join(viewed_city)
                print(coockie_data)
            except:
                coockie_data = city
            resp.set_cookie('viewed_city', coockie_data,  max_age=60 * 60 * 24 * 14)
            return resp
        else:
            return jsonify({
                'success': False,
            })
    except:
        return jsonify({
            'success': False,
        })
if __name__ == '__main__':
    app.run(debug=True)
