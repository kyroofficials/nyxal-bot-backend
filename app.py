from flask import Flask, jsonify, request
from flask_cors import CORS
import discord
from discord.ext import commands
import os
import asyncio
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot_data = {
    'status': 'online',
    'activity': 'NyXal Bot Dashboard',
    'start_time': datetime.now()
}

# === API ROUTES ===
@app.route('/')
def home():
    return jsonify({'message': 'NyXal Bot API is running!', 'status': 'online'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'guild_count': len(bot.guilds),
        'user_count': len(bot.users),
        'uptime': str(datetime.now() - bot_data['start_time']),
        'status': bot_data['status'],
        'latency': round(bot.latency * 1000) if bot.latency else 0
    })

@app.route('/api/servers', methods=['GET'])
def get_servers():
    servers = []
    for guild in bot.guilds:
        servers.append({
            'id': str(guild.id),
            'name': guild.name,
            'member_count': guild.member_count,
            'icon': str(guild.icon.url) if guild.icon else None
        })
    return jsonify({'servers': servers})

@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.json
    # ... (sama seperti code sebelumnya)
    return jsonify({'success': True, 'message': 'Status updated'})

# === BOT EVENTS & COMMANDS ===
@bot.event
async def on_ready():
    print(f'🎉 {bot.user} is ready!')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers | !help"
        )
    )

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

def run_bot():
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
