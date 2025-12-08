from flask import Flask
import redis
import os

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    count = cache.incr('hits')
    
    hostname = os.environ.get('HOSTNAME', 'unknown')
    
    return f'''
    <html>
    <head>
        <title>Счётчик посещений</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #71b280 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                color: white;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                padding: 40px 60px;
                border-radius: 20px;
                text-align: center;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            h1 {{ font-size: 3em; margin-bottom: 10px; }}
            .count {{ 
                font-size: 5em; 
                font-weight: bold; 
                color: #00d4ff;
                text-shadow: 0 0 20px rgba(0,212,255,0.5);
            }}
            .hostname {{
                margin-top: 20px;
                padding: 10px;
                background: rgba(0,0,0,0.2);
                border-radius: 10px;
                font-family: monospace;
            }}
            .version {{
                margin-top: 15px;
                font-size: 0.9em;
                opacity: 0.7;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛒 Интернет-магазин</h1>
            <p>Количество посещений:</p>
            <div class="count">{count}</div>
            <div class="hostname">
                Обслуживает контейнер: <strong>{hostname}</strong>
            </div>
            <div class="version">Версия: v2 (зеленый)</div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

