from flask import Flask, send_from_directory, jsonify, request, redirect
from flask_cors import CORS
import os
import requests
import re

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

STEAM_KEY = os.environ.get('STEAM_KEY')


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')


@app.route('/api/games')
def api_games():
    # placeholder local
    games = [
        {"id":570, "name":"Dota 2", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg"},
        {"id":730, "name":"Counter-Strike: Global Offensive", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg"},
        {"id":440, "name":"Team Fortress 2", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg"}
    ]
    return jsonify(games)


@app.route('/api/trending')
def api_trending():
    # Mais jogados hoje (mock)
    games = [
        {"id":570, "name":"Dota 2", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg", "count":"125k jogando"},
        {"id":730, "name":"Counter-Strike: Global Offensive", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg", "count":"98k jogando"},
        {"id":1391110, "name":"Palworld", "price":"$29.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1391110/header.jpg", "count":"72k jogando"},
        {"id":2105470, "name":"Black Myth: Wukong", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2105470/header.jpg", "count":"65k jogando"},
    ]
    return jsonify(games)


@app.route('/api/recent')
def api_recent():
    # Recém lançados (mock)
    games = [
        {"id":2105470, "name":"Black Myth: Wukong", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2105470/header.jpg", "date":"21 fev 2026"},
        {"id":1950570, "name":"Tekken 8", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1950570/header.jpg", "date":"12 fev 2026"},
        {"id":2120430, "name":"Indiana Jones and the Great Circle", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2120430/header.jpg", "date":"08 fev 2026"},
        {"id":2062160, "name":"Metaphor: ReFantazio", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2062160/header.jpg", "date":"04 fev 2026"},
    ]
    return jsonify(games)


@app.route('/api/categories')
def api_categories():
    # Categorias de jogos
    return jsonify({
        "all": [
            {"id":570, "name":"Dota 2", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg", "category":"action"},
            {"id":730, "name":"Counter-Strike: Global Offensive", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg", "category":"action"},
            {"id":1391110, "name":"Palworld", "price":"$29.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1391110/header.jpg", "category":"rpg"},
            {"id":2105470, "name":"Black Myth: Wukong", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2105470/header.jpg", "category":"action"},
            {"id":1950570, "name":"Tekken 8", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1950570/header.jpg", "category":"action"},
            {"id":2062160, "name":"Metaphor: ReFantazio", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2062160/header.jpg", "category":"rpg"},
            {"id":200210, "name":"Total War: WARHAMMER II", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/200210/header.jpg", "category":"strategy"},
            {"id":570560, "name":"Valheim", "price":"$19.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570560/header.jpg", "category":"simulation"},
            {"id":552520, "name":"Portal 2", "price":"$9.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/620/header.jpg", "category":"puzzle"},
            {"id":1097840, "name":"Portal 2", "price":"$9.99", "img":"https://via.placeholder.com/360x200", "category":"puzzle"},
        ],
        "action": [
            {"id":730, "name":"Counter-Strike: Global Offensive", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg", "category":"action"},
            {"id":570, "name":"Dota 2", "price":"Free", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg", "category":"action"},
            {"id":2105470, "name":"Black Myth: Wukong", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2105470/header.jpg", "category":"action"},
            {"id":1950570, "name":"Tekken 8", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1950570/header.jpg", "category":"action"},
        ],
        "rpg": [
            {"id":1391110, "name":"Palworld", "price":"$29.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/1391110/header.jpg", "category":"rpg"},
            {"id":2062160, "name":"Metaphor: ReFantazio", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/2062160/header.jpg", "category":"rpg"},
            {"id":431960, "name":"The Witcher 3", "price":"$39.99", "img":"https://via.placeholder.com/360x200", "category":"rpg"},
        ],
        "strategy": [
            {"id":200210, "name":"Total War: WARHAMMER II", "price":"$59.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/200210/header.jpg", "category":"strategy"},
            {"id":8980, "name":"Sid Meier's Civilization V", "price":"$49.99", "img":"https://via.placeholder.com/360x200", "category":"strategy"},
        ],
        "puzzle": [
            {"id":552520, "name":"Portal 2", "price":"$9.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/620/header.jpg", "category":"puzzle"},
            {"id":289740, "name":"Bejeweled 3", "price":"$9.99", "img":"https://via.placeholder.com/360x200", "category":"puzzle"},
        ],
        "simulation": [
            {"id":570560, "name":"Valheim", "price":"$19.99", "img":"https://cdn.cloudflare.steamstatic.com/steam/apps/570560/header.jpg", "category":"simulation"},
            {"id":644930, "name":"Cities: Skylines", "price":"$39.99", "img":"https://via.placeholder.com/360x200", "category":"simulation"},
        ]
    })
def api_achievements():
    # Conquistas mock (em produção, vêm do banco de dados/perfil do usuário)
    achievements = [
        {"id":1, "name":"Primeiro Passo", "desc":"Faça seu primeiro login", "unlocked":True, "icon":"🎮"},
        {"id":2, "name":"Comprador", "desc":"Realize sua primeira compra", "unlocked":True, "icon":"🛒"},
        {"id":3, "name":"Colecionador", "desc":"Tenha 10 jogos na biblioteca", "unlocked":True, "icon":"📚"},
        {"id":4, "name":"Fã de Ação", "desc":"Compre 5 jogos de ação", "unlocked":False, "icon":"⚔️"},
        {"id":5, "name":"Estrategista", "desc":"Compre 3 jogos estratégia", "unlocked":True, "icon":"♟️"},
        {"id":6, "name":"Explorador", "desc":"Compre em todas as categorias", "unlocked":False, "icon":"🗺️"},
    ]
    return jsonify(achievements)


@app.route('/api/achievements/stats')
def api_achievements_stats():
    # Estatísticas e desconto baseado em conquistas
    achievements = api_achievements  # chama a função
    resp = achievements()
    if isinstance(resp, tuple):
        return resp
    achievements_list = resp.get_json() if hasattr(resp, 'get_json') else resp
    if not isinstance(achievements_list, list):
        achievements_list = []
    unlocked_count = sum(1 for a in achievements_list if a and a.get('unlocked'))
    discount_percent = min(unlocked_count * 5, 50)
    return jsonify({
        "total": len(achievements_list),
        "unlocked": unlocked_count,
        "discount_percent": discount_percent
    })


@app.route('/api/game/<int:game_id>')
def api_game_detail(game_id):
    return jsonify({
        "id": game_id,
        "name": f"Jogo {game_id}",
        "description": "Descrição de exemplo para demonstração.",
        "price": "Grátis",
    })


def get_owned_games(steamid):
    if not STEAM_KEY:
        return {'error': 'STEAM_KEY não configurada'}, 500
    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
    params = {'key': STEAM_KEY, 'steamid': steamid, 'include_appinfo': 1, 'include_played_free_games': 1}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get('response', {}).get('games', [])


def get_app_details(appid):
    url = 'https://store.steampowered.com/api/appdetails'
    r = requests.get(url, params={'appids': appid, 'cc': 'BR', 'l': 'portuguese'}, timeout=8)
    if r.status_code != 200:
        return None
    data = r.json().get(str(appid), {})
    if not data.get('success'):
        return None
    return data.get('data')


@app.route('/api/steam-games/<steamid>')
def api_steam_games(steamid):
    if not steamid or not str(steamid).isdigit():
        return jsonify({'error': 'steamid inválido'}), 400
    try:
        games = get_owned_games(steamid)
        if isinstance(games, tuple):
            return games
    except Exception as e:
        return jsonify({'error': f'Steam API indisponível: {str(e)}'}), 500
    if not games:
        return jsonify({'error': 'Perfil privado ou sem jogos'}), 200
    # enriquecer apenas primeiros 30 para não sobrecarregar
    for g in games[:30]:
        g['cover'] = f'https://cdn.cloudflare.steamstatic.com/steam/apps/{g["appid"]}/header.jpg'
        details = get_app_details(g['appid'])
        if details:
            g['store'] = {'name': details.get('name'), 'short_description': details.get('short_description')}
    return jsonify(games)


# OpenID Steam (login)
@app.route('/auth/steam/login')
def steam_login():
    host = request.host_url.rstrip('/')
    return_to = f"{host}/auth/steam/validate"
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': return_to,
        'openid.realm': host,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }
    redirect_url = 'https://steamcommunity.com/openid/login?' + '&'.join([f"{k}={requests.utils.requote_uri(v)}" for k, v in params.items()])
    return redirect(redirect_url)


@app.route('/auth/steam/validate')
def steam_validate():
    try:
        # Verifica resposta OpenID com Steam
        data = {k: request.args.get(k) for k in request.args}
        if not data:
            return jsonify({'error': 'Sem parâmetros OpenID'}), 400
        # prepare payload for verification
        payload = {k: v for k, v in data.items()}
        payload['openid.mode'] = 'check_authentication'
        verify = requests.post('https://steamcommunity.com/openid/login', data=payload, timeout=8)
        if verify.status_code != 200 or 'is_valid:true' not in verify.text:
            return jsonify({'error': 'Falha na verificação OpenID'}), 400
        claimed_id = data.get('openid.claimed_id') or data.get('openid.identity')
        if not claimed_id:
            return jsonify({'error': 'claimed_id não encontrado'}), 400
        m = re.search(r"/id/(\d+)", claimed_id)
        if not m:
            return jsonify({'error': 'steamid não encontrado na claimed_id'}), 400
        steamid = m.group(1)
        # redireciona para a homepage com steamid como query param (frontend pode usá-lo)
        return redirect(f"/?steamid={steamid}")
    except Exception as e:
        return jsonify({'error': f'Erro OpenID: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

