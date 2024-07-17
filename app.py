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
                viewed_cities = viewed_city.split('/')[-1:-6:-1]

            else:
                viewed_cities.extend(viewed_city.split('/')[::-1])

    except:
        city = 'Москва'

    weather = get_weather(city, time)


    return render_template('index.html', weather=weather, city=city, viewed_cities=viewed_cities)


@app.route('/changeCity', methods=['POST'])
def changeCity():
    city = request.json.get('city')
    if get_weather(city):
        resp = make_response(jsonify({
            'success': True,
        }))
        resp.set_cookie('user_city', city)
        viewed_city = request.cookies.get('viewed_city').split('/')
        print(viewed_city)
        if len(viewed_city) > 5:
            viewed_city = viewed_city[-1:-5:-1][::-1]
        viewed_city.append(city)
        coockie_data = '/'.join(viewed_city)
        print(coockie_data)
        resp.set_cookie('viewed_city', coockie_data,  max_age=60 * 60 * 24 * 14)
        return resp
    else:
        return jsonify({
            'success': False,
        })
if __name__ == '__main__':
    app.run(debug=True)
